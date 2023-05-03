import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
import sqlite3, random, shutil, os
from src.gui.bulkcollector import BulkCollector
from src.constants import *


class Manager(tk.Tk):
    conn:sqlite3.Connection=None
    cursor:sqlite3.Cursor = None

    imagePath = None
    
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        self.setup_ui()
        self.conn.commit()
        self.conn.close()

    def setup_ui(self) -> None:
        self.resizable(0, 0)
        self.title("data collector")

        topFrame = tk.LabelFrame(self, text="Category")
        topFrame.pack(padx=10, pady=10, fill="both")


        self.list_cate = self.getCategory()
        self.cate_select = ttk.Combobox(topFrame, values=self.list_cate, width=20)
        if len(self.list_cate) != 0:   self.cate_select.current(0)
        self.cate_select.grid(row=0, column=0, padx=5, pady=5)

        tk.Button(topFrame, text="Load", command=self.loadCate, width=15).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(topFrame, text="New", command= self.addCategory, width=15).grid(row=0, column=2, padx=5, pady=5)

        tk.Button(topFrame, text="Delete", command=self.deleteCategory, width=15).grid(row=0, column=3, padx=5, pady=5)

        listFrame = tk.Frame(self)
        listFrame.pack(fill="both")

        self.tree = ttk.Treeview(listFrame, show="headings", selectmode="browse", columns=("id", "text"))
        self.tree.pack(padx=10, pady=10, fill="both", expand=True, side=tk.LEFT)

        self.tree.column("id", width=30, stretch=False, minwidth=30)

        self.tree.heading("id", text="Id")

        scrollbar = ttk.Scrollbar(listFrame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.tree.yview)

        self.loadCate()

        middleFrame = tk.LabelFrame(self, text="text")
        middleFrame.pack(padx=10, pady=10, fill="both")

        def delete():
            selected_item = self.tree.selection()
            if selected_item:
                cate = self.cate_select.get()
                item = self.tree.item(selected_item, "values")
                img = self.cursor.execute(f"SELECT image from {cate} WHERE id={item[0]}").fetchone()
                os.remove(img[0])
                self.cursor.execute(f"DELETE FROM {cate} WHERE id={item[0]}")
                self.conn.commit()
                self.loadCate() 

        saveBtn = tk.Button(middleFrame, text="Delete", command=delete)
        saveBtn.grid(row=0, column=0, padx=5, pady=5)

        def bulkColl() :    BulkCollector(self.cate_select.get(), self.cursor, self.conn)

        tk.Button(middleFrame, text="Collector", command=bulkColl).grid(row=0, column=1, padx=5, pady=5)

        self.mainloop()

    def getCategory(self):
        tables = self.cursor.execute("select name from sqlite_master where type='table';").fetchall()
        if tables.count(('sqlite_sequence',)) > 0:
            tables.remove(('sqlite_sequence',))
        return tables
    
    def addCategory(self):
        root = tk.Toplevel(self)
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
            self.cate_select["values"] = self.getCategory()
            root.destroy()

        tk.Button(root, text="create", command=create).pack(fill="both", padx=10, pady=10)

    def deleteCategory(self):
        category = self.cate_select.get()
        res = messagebox.askyesno(f"Delete '{category}'", f"are you sure to delete '{category}'")
        if res:
            list_imgs = self.cursor.execute(f"SELECT image from {category}").fetchall()
            for img in list_imgs:   os.remove(img[0])
            self.cursor.execute(f"DROP TABLE {category}")
            self.conn.commit()
            self.cate_select["values"] = self.getCategory()
            self.cate_select.current(0)

    def loadCate(self):
        cate = self.cate_select.get()
        if cate != "":
            self.tree.heading("text", text=cate)
            for item in self.tree.get_children():    self.tree.delete(item)
            texts = self.cursor.execute(f"select id, text from {cate};").fetchall()
            for text in texts:  self.tree.insert("", tk.END, values=text)
