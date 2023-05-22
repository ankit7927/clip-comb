import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3, os, shutil, sys
from src.constants import *
from shutil import make_archive, unpack_archive
from src.collector import Collector
from src.hometab import HomeUI
from src.creatortab import CreatorUI

class ClipComb(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.set_ui()

    def set_ui(self) -> None:
        self.conn = sqlite3.connect(DB_PATH)

        self.title(APP_NAME)
        self.geometry("600x400")
        self.resizable(0, 0)

        menubar = tk.Menu(self)

        cate_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Category", menu=cate_menu)

        cate_menu.add_command(label="New", command=self.addCategory)
        cate_menu.add_command(label="Delete", command=self.deleteCategory)
        cate_menu.add_separator()
        cate_menu.add_command(label="Import", command=self.import_db)
        cate_menu.add_command(label="Export", command=self.export_db)

        menubar.add_command(label="Collector", command=lambda : Collector(self.conn))

        self.config(menu=menubar)

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)

        notebook.add(tab1, text="Home")
        notebook.add(tab2, text="Create")

        HomeUI(tab1, self.conn)

        CreatorUI(tab2, self.conn)

        self.mainloop()
        self.conn.commit()


    def removeOld(self):
        if self.delete:
            for i in self.removable:
                fname = self.conn.execute(IMAGE_WITH_ID(self.cate, i)).fetchone()
                os.remove(fname[0])
                self.conn.execute(DELETE_ROW(self.cate, i))
            print("removed old")

    def export_db(self):
        make_archive(ZIP_NAME, base_dir=DB_DIR, format="zip", root_dir=".")

    def import_db(self):
        filetypes = (ARCHIVE_FILE_TUP, ALL_FILES_TUP)
        zipdir = filedialog.askopenfilename(title="Select Background", filetypes=filetypes)
        if zipdir:
            if os.path.isdir(DB_DIR):
                self.conn.close()
                shutil.rmtree(DB_DIR)
            unpack_archive(zipdir, ".", "zip")
            sys.exit(0)

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
            self.conn.execute(CREATE_TABLE(cat))
            root.destroy()
            self.quit()

        tk.Button(root, text="create", command=create).pack(fill="both", padx=10, pady=10)
    
    def deleteCategory(self):
        if self.cate is not None:
            res = messagebox.askyesno(f"Delete '{self.cate}'", f"are you sure to delete '{self.cate}'")
            if res:
                try:
                    list_imgs = self.conn.execute(ALL_IMAGE(self.cate)).fetchall()
                    for img in list_imgs:   os.remove(img[0])
                    self.conn.execute(DROP_TABLE(self.cate))
                    self.quit()
                except Exception as e:
                    print(e)