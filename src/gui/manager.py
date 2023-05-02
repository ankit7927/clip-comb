import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
import sqlite3, random, shutil, os
from src.gui.bulkcollector import BulkCollector
from src.constants import *


class Manager:
    conn:sqlite3.Connection=None
    cursor:sqlite3.Cursor = None

    imagePath = None
    
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        self.gui()
        self.conn.commit()
        self.conn.close()

    def gui(self):
        root = tk.Tk()
        root.resizable(0, 0)
        root.title("data collector")

        topFrame = tk.LabelFrame(root, text="Category")
        topFrame.pack(padx=10, pady=10, fill="both")


        list_cate = self.getCategory()
        cate_select = ttk.Combobox(topFrame, values=list_cate, width=20)
        if len(list_cate) != 0:   cate_select.current(0)
        cate_select.grid(row=0, column=0, padx=5, pady=5)

        loadCateg = tk.Button(topFrame, text="Load", command=lambda: self.loadCate(cate_select.get(), tree))
        loadCateg.grid(row=0, column=1, padx=5, pady=5)

        addCatBtn = tk.Button(topFrame, text="New", command=lambda: self.addCategory(root))
        addCatBtn.grid(row=0, column=2, padx=5, pady=5)

        tk.Button(topFrame, text="Delete", command=lambda: self.deleteCategory(root, cate_select.get())).grid(row=0, column=3, padx=5, pady=5)

        def bulkColl() : BulkCollector(cate_select.get(), self.cursor, self.conn)

        tk.Button(topFrame, text="Collector", command=bulkColl).grid(row=0, column=4, padx=5, pady=5)

        listFrame = tk.Frame(root)
        listFrame.pack(fill="both")

        tree = ttk.Treeview(listFrame, show="headings", selectmode="browse", columns=("id", "text"))
        tree.pack(padx=10, pady=10, fill="both", expand=True, side=tk.LEFT)

        tree.column("id", width=30, stretch=False, minwidth=30)

        tree.heading("id", text="Id")

        scrollbar = ttk.Scrollbar(listFrame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=tree.yview)

        self.loadCate(cate_select.get(), tree)

        middleFrame = tk.LabelFrame(root, text="text")
        middleFrame.pack(padx=10, pady=10, fill="both")

        text_entry = tk.Entry(middleFrame, width=60)
        text_entry.grid(row=0, column=0, padx=5, pady=5)

        def chooseimage():
            filetypes = (("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*"))
            self.imagePath = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)

        imageBtn = tk.Button(middleFrame, text="Image", command=chooseimage)
        imageBtn.grid(row=0, column=1, padx=5, pady=5)

        saveBtn = tk.Button(middleFrame, text="Save And Add Another", width=60, command=lambda: self.addText(cate_select.get(), tree, text_entry))
        saveBtn.grid(row=1, column=0, padx=5, pady=5)

        def delete():
            selected_item = tree.selection()
            if selected_item:
                cate = cate_select.get()
                item = tree.item(selected_item, "values")
                img = self.cursor.execute(f"SELECT image from {cate} WHERE id={item[0]}").fetchone()
                os.remove(img[0])
                self.cursor.execute(f"DELETE FROM {cate} WHERE id={item[0]}")
                self.conn.commit()
                self.loadCate(cate, tree) 

        saveBtn = tk.Button(middleFrame, text="Delete", command=delete)
        saveBtn.grid(row=1, column=1, padx=5, pady=5)

        root.mainloop()

    def getCategory(self):
        tables = self.cursor.execute("select name from sqlite_master where type='table';").fetchall()
        if tables.count(('sqlite_sequence',)) > 0:
            table = tables.remove(('sqlite_sequence',))
        return tables
    
    def addCategory(self, master):
        root = tk.Toplevel(master)
        root.title("Create New Category")

        tk.Label(root, text="Enter Category Name").pack(fill="both", padx=10, pady=10)

        cate = tk.Entry(root)
        cate.pack(fill="both", padx=10, pady=10)

        def create():
            cat = cate.get()
            if cat == "":
                messagebox.showerror("Bad name", "name should be not empty")
                return
            cat = cat.replace(" ", "_")
            self.cursor.execute(f"create table {cat} (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, image TEXT)")
            self.conn.commit()
            master.destroy()

        tk.Button(root, text="create", command=create).pack(fill="both", padx=10, pady=10)

    def deleteCategory(self, master, category):
        res = messagebox.askyesno(f"Delete '{category}'", f"are you sure to delete '{category}' \n\ndeleting will close the appliction")
        if res:
            list_imgs = self.cursor.execute(f"SELECT image from {category}").fetchall()
            for img in list_imgs:   os.remove(img[0])
            self.cursor.execute(f"DROP TABLE {category}")
            self.conn.commit()
            master.destroy()

    def loadCate(self, cate, tree):
        if cate != "":
            tree.heading("text", text=cate)
            for item in tree.get_children():    tree.delete(item)
            texts = self.cursor.execute(f"SELECT id, text FROM {cate};").fetchall()
            for text in texts:  tree.insert("", tk.END, values=text)


    def addText(self, category, tree, text_entry):
        text = text_entry.get()
        if text_entry.get() =="" or self.imagePath == None:
            messagebox.showwarning("Bad Entry", "both text and image required")
            return
        
        imageid = random.randint(10000000, 99999999)
        imageid = str(imageid)+"."+self.imagePath.split(".")[1]

        img_path = shutil.copyfile(self.imagePath, IMAGES_DIR+imageid)
        
        self.cursor.execute(f"INSERT INTO {category} VALUES(?, ?, ?)", (None, text, img_path, ))
        
        self.conn.commit()

        tree.insert("", tk.END, values=(self.cursor.lastrowid, text))

        text_entry.delete(0, tk.END)
        self.imagePath = None
