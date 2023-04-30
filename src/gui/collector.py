import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
import sqlite3, os


class Collector:
    data:list = []
    backPath:str = None
    font:str = None

    removable:dict = {}

    conn:sqlite3.Connection=None
    cursor:sqlite3.Cursor = None

    imagePath = None

    def __init__(self) -> None:
        self.conn = sqlite3.connect("src/db/shorts.db")
        self.cursor = self.conn.cursor()

        self.gui()
        self.conn.commit()

    def gui(self) -> None:
        root = tk.Tk()
        root.resizable(0, 0)
        root.title("data collector")

        topFrame = tk.LabelFrame(root, text="Category")
        topFrame.pack(padx=10, pady=10, fill="both")

        list_cate = self.getCategory()
        cate_select = ttk.Combobox(topFrame, values=list_cate, width=20)
        if len(list_cate) != 0:   cate_select.current(0)
        cate_select.grid(row=0, column=0, padx=5, pady=5)


        load_cate = tk.Button(topFrame, text="Load Category", command=lambda: self.loadCate(cate_select.get(), tree))
        load_cate.grid(row=0, column=1, padx=5, pady=5)

        listFrame = tk.Frame(root)
        listFrame.pack(fill="both")

        tree = ttk.Treeview(listFrame, show="headings", selectmode="browse", columns=("id", "text"))
        tree.pack(padx=10, pady=10, fill="both", expand=True, side=tk.LEFT)

        tree.column("id", width=30, stretch=False, minwidth=30)

        tree.heading("id", text="Id")

        scrollbar = ttk.Scrollbar(listFrame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=tree.yview)

        self.loadCate(cate_select.get(), tree)

        middleFrame = tk.LabelFrame(root, text="Creation")
        middleFrame.pack(padx=10, pady=10, fill="both")

        titleEntry = tk.Entry(middleFrame, width=50)
        titleEntry.grid(padx=10, pady=10, row=0, column=0)

        def select_image():
            filetypes = (("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*"))
            self.imagePath = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)

        imageBtn = tk.Button(middleFrame, text="Image", command=select_image)
        imageBtn.grid(padx=10, pady=10, row=0, column=1)

        def select_back():
            filetypes = (("Video file", "*.mp4"), ("All files", "*.*"))
            self.backPath = filedialog.askopenfilename(title="Select Background", filetypes=filetypes)

        backBtn = tk.Button(middleFrame, text="Background", command=select_back)
        backBtn.grid(padx=10, pady=10, row=0, column=2)

        fonts = os.listdir("src/fonts")
        font_select = ttk.Combobox(middleFrame, values=fonts, width=40)
        font_select.current(0)
        font_select.grid(row=1, column=0, padx=10, pady=5)

        text_selection = [i for i in range(3, 11)]
        text_count_select = ttk.Combobox(middleFrame, values=text_selection, width=10)
        text_count_select.current(0)
        text_count_select.grid(row=1, column=1, padx=10, pady=5)

        createBtn = tk.Button(middleFrame, text="Start Creating", 
                              command=lambda: self.create(titleEntry, font_select.get(), text_count_select.get(), cate_select.get(), root))
        
        createBtn.grid(padx=10, pady=5, row=1, column=2)

        root.mainloop()

    def getCategory(self):
        return self.cursor.execute("select name from sqlite_master where type='table';").fetchall()
    
    def loadCate(self, cate, tree):
        if cate != "":
            tree.heading("text", text=cate)
            for item in tree.get_children():    tree.delete(item)
            texts = self.cursor.execute(f"select id, text from {cate};").fetchall()
            for text in texts:  tree.insert("", tk.END, values=text)

    def create(self, title, font, count, cate, master):
        if title.get() == "":
            messagebox.showerror("Bad entry", "Title is required")
            return
        elif self.imagePath == None:
            messagebox.showerror("Bad Selection", "title image required")
            return
        elif self.backPath == None:
            messagebox.showerror("Bad Selection", "Background is required")
            return
        
        self.font = font

        self.data.insert(0, {"text":title.get(), "image":self.imagePath})

        records = self.cursor.execute(f"SELECT * FROM {cate}").fetchmany(int(count))

        self.removable= {"cate":cate, "remove":[]}
        for rec in records:
            self.removable["remove"].append(rec[0])
            self.data.append({"text":rec[1], "image":rec[2]})

        title.delete(0, tk.END)
        
        master.destroy()

    def get(self):
        return (self.data, self.backPath, self.font)
    
    def removeOld(self):
        cate = self.removable["cate"]
        for i in self.removable["remove"]:
            self.cursor.execute(f"DELETE FROM {cate} WHERE id={i}")
        print("removed old")
        self.conn.commit()
        self.conn.close()
