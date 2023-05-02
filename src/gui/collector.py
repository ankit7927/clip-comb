import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
import sqlite3, os
from src.constants import *
from shutil import make_archive, unpack_archive

class Collector(tk.Tk):
    data:list = []
    backPath:str = None
    font:str = None

    removable:dict = {}

    conn:sqlite3.Connection=None
    cursor:sqlite3.Cursor = None

    titlePath = None

    def __init__(self) -> None:
        super().__init__()
        self.set_ui()

    def set_ui(self) -> None:
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        ###
        self.title("Shorts Maker")
        self.resizable(0, 0)

        topFrame = tk.LabelFrame(self, text="Category")
        topFrame.pack(padx=10, pady=10, fill="both")

        self.list_cate = self.getCategory()
        self.cate_select = ttk.Combobox(topFrame, values=self.list_cate, width=20)
        if len(self.list_cate) != 0:   self.cate_select.current(0)
        self.cate_select.grid(row=0, column=0, padx=5, pady=5)

        tk.Button(topFrame, text="Load Category", command=self.loadCate).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(topFrame, text="Import", command=self.import_db).grid(row=0, column=2, padx=5, pady=5)

        tk.Button(topFrame, text="Export", command=self.export).grid(row=0, column=3, padx=5, pady=5)

        listFrame = tk.Frame(self)
        listFrame.pack(fill="both")

        self.tree = ttk.Treeview(listFrame, show="headings", selectmode="browse", columns=("id", "text"))
        self.tree.pack(padx=10, pady=10, fill="both", expand=True, side=tk.LEFT)

        self.tree.column("id", width=30, stretch=False, minwidth=30)
        self.tree.heading("id", text="Id")

        scrollbar = ttk.Scrollbar(listFrame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.tree.yview)

        self.loadCate()

        middleFrame = tk.LabelFrame(self, text="Creation")
        middleFrame.pack(padx=10, pady=10, fill="both")

        self.titleEntry = tk.Entry(middleFrame, width=50)
        self.titleEntry.grid(padx=10, pady=10, row=0, column=0)

        imageBtn = tk.Button(middleFrame, text="Image", command=lambda:self.select_media(type="title"))
        imageBtn.grid(padx=10, pady=10, row=0, column=1)

        backBtn = tk.Button(middleFrame, text="Background", command=lambda:self.select_media(type="back"))
        backBtn.grid(padx=10, pady=10, row=0, column=2)

        fonts = os.listdir(FONTS_DIR)
        self.font_select = ttk.Combobox(middleFrame, values=fonts, width=40)
        self.font_select.current(0)
        self.font_select.grid(row=1, column=0, padx=10, pady=5)

        text_selection = [i for i in range(3, 11)]
        self.text_count_select = ttk.Combobox(middleFrame, values=text_selection, width=10)
        self.text_count_select.current(0)
        self.text_count_select.grid(row=1, column=1, padx=10, pady=5)

        createBtn = tk.Button(middleFrame, text="Start Creating", command=self.create)
        createBtn.grid(padx=10, pady=5, row=1, column=2)

        self.mainloop()
        self.conn.commit()

    def select_media(self, type):
            if type == "back":
                filetypes = (("Video file", "*.mp4"), ("All files", "*.*"))
                self.backPath = filedialog.askopenfilename(title="Select Background", filetypes=filetypes)
            elif type == "title":
                filetypes = (("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*"))
                self.titlePath = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)

    def getCategory(self):
        tables = self.cursor.execute("select name from sqlite_master where type='table';").fetchall()
        if tables.count(('sqlite_sequence',)) > 0:
            tables.remove(('sqlite_sequence',))
        return tables
    
    def loadCate(self):
        cate = self.cate_select.get()
        if cate != "":
            self.tree.heading("text", text=cate)
            for item in self.tree.get_children():    self.tree.delete(item)
            texts = self.cursor.execute(f"select id, text from {cate};").fetchall()
            for text in texts:  self.tree.insert("", tk.END, values=text)

    def create(self):
        if self.titleEntry.get() == "":
            messagebox.showerror("Bad entry", "Title is required")
            return
        elif self.titlePath == None:
            messagebox.showerror("Bad Selection", "title image required")
            return
        elif self.backPath == None:
            messagebox.showerror("Bad Selection", "Background is required")
            return
        
        cate = self.cate_select.get()
        self.font = self.font_select.get()

        self.data.insert(0, {"text":self.titleEntry.get(), "image":self.titlePath})

        records = self.cursor.execute(f"SELECT * FROM {cate}").fetchmany(int(self.text_count_select.get()))

        self.removable= {"cate":cate, "remove":[]}
        for rec in records:
            self.removable["remove"].append(rec[0])
            self.data.append({"text":rec[1], "image":rec[2]})

        self.titleEntry.delete(0, tk.END)
        
        self.destroy()

    def get(self):
        return (self.data, self.backPath, self.font)
    
    def removeOld(self):
        cate = self.removable["cate"]
        for i in self.removable["remove"]:
            fname = self.cursor.execute(f"SELECT image FROM {cate} WHERE id={i}").fetchone()
            os.remove(fname[0])
            self.cursor.execute(f"DELETE FROM {cate} WHERE id={i}")
        print("removed old")
        self.conn.commit()
        self.conn.close()

    def export(self):
        make_archive(ZIP_NAME, base_dir=DB_DIR, format="zip", root_dir=".")

    def import_db(self):
        filetypes = (("Archive file", "*.zip"), ("All files", "*.*"))
        zipdir = filedialog.askopenfilename(title="Select Background", filetypes=filetypes)
        if zipdir:
            unpack_archive(zipdir, ".", "zip")