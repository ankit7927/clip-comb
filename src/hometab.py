import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import ttk, filedialog, messagebox
import os, shutil, sys
from shutil import make_archive, unpack_archive
from src.constants import *
from src.collector import Collector
import os, requests



class HomeUI:

    def __init__(self, tab, conn) -> None:
        self.conn = conn
        self.root = tab

        self.initUI()

    def initUI(self) -> None:
        
        self.tree = ttk.Treeview(self.root, show="headings", selectmode="browse", columns=("id", "text"))
        self.tree.pack(fill="both", expand=True, side=tk.LEFT, padx=10, pady=10)

        self.tree.column("id", width=40, stretch=False, minwidth=40)
        self.tree.heading("id", text="Id")
        self.tree.heading("text", text="Texts")


        buttonframe = tk.Frame(self.root)
        buttonframe.pack(fill=tk.BOTH, side=tk.RIGHT)

        categories =  self.getCategory()
        category_var = tk.StringVar()
        category_var.set("Category")
        category_menu = tk.OptionMenu(buttonframe, category_var, command=lambda e:self.loadCate(e), *categories)
        category_menu.config(width=15)
        category_menu.pack(padx=5, pady=5, fill=tk.X)

        tk.Button(buttonframe, text="Delete", command=self.delete_item).pack(padx=5, pady=5, fill=tk.X)

        tk.Button(buttonframe, text="Update", command=self.update_item).pack(padx=5, pady=5, fill=tk.X)


        tk.Button(buttonframe, text="Collector", command=lambda: Collector(self.conn)).pack(padx=5, pady=25, fill=tk.X)


        tk.Button(buttonframe, text="New", command=self.addCategory).pack(padx=5, pady=5, fill=tk.X)

        tk.Button(buttonframe, text="Delete", command=self.deleteCategory).pack(padx=5, pady=5, fill=tk.X)

        tk.Button(buttonframe, text="Import", command=self.import_db).pack(padx=5, pady=5, fill=tk.X)

        tk.Button(buttonframe, text="Export", command=self.export_db).pack(padx=5, pady=5, fill=tk.X)



    def getCategory(self) -> list:
        tables = self.conn.execute(ALL_TABLE_QUERY).fetchall()
        if len(tables) == 0:
            return ["#None"]
        if tables.count((SEQUENCE_TABLE_NAME,)) > 0:
            tables.remove((SEQUENCE_TABLE_NAME,))
        return [table[0] for table in tables]

    def loadCate(self, cate) -> None:
        if cate == "#None":
            return
        if cate != "":
            self.cate = cate
            for item in self.tree.get_children():
                self.tree.delete(item)
            texts = self.conn.execute(TEXT_ID_FROM_CATEGORY(cate)).fetchall()
            for text in texts:
                self.tree.insert("", tk.END, values=text)

    def delete_item(self) -> None:
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item, "values")
            self.conn.execute(DELETE_ROW(self.cate, item[0]))
            self.loadCate(self.cate)
    
    def update_item(self) -> None:
        selected_item = self.tree.selection()
        if selected_item:
            itemID = self.tree.item(selected_item, "values")[0]
            item = self.conn.execute(TEXT_SELECTION_QUERY(self.cate, itemID)).fetchone()

            def update():
                text = text_entry.get()
                image_link = img_link.get()
                if text == "":
                    messagebox.showerror("bad entry", "both fields are required")
                    return

                self.conn.execute(UPDATE_ROW_TEXT(self.cate), (text, item[0]))

                if image_link != "":
                    self.conn.execute(UPDATE_ROW_IMAGE(self.cate), (image_link, item[0], ))

                root.destroy()

            root = tk.Toplevel(self.root)

            text_entry = tk.Entry(root, width=40)
            text_entry.pack(padx=10, pady=10)
            text_entry.insert(0, item[1])

            img_link = tk.Entry(root, width=40)
            img_link.pack(padx=10, pady=10)

            tk.Button(root, text="Update", command=update).pack(padx=10, pady=10)

            root.mainloop()

    def removeOld(self):
        if self.delete:
            for i in self.removable:
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
        root = tk.Toplevel(self.root)
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
                self.conn.execute(DROP_TABLE(self.cate))