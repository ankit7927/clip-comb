import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3, os, requests, shutil, sys
from src.constants import *
from shutil import make_archive, unpack_archive
from src.collector import Collector
from src.tab1 import Tab1UI
from src.tab2 import Tab2UI

class ClipComb(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.set_ui()

    def set_ui(self) -> None:
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

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
        cate_menu.add_command(label="Export", command=self.export)

        menubar.add_command(label="Collector", command=self.opencollector)

        self.config(menu=menubar)

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)

        notebook.add(tab1, text="Home")
        notebook.add(tab2, text="Create")

        ## tab 1 
        Tab1UI(tab1, self.conn)

        ### tab2 
        Tab2UI(tab2, self.conn)

        self.mainloop()
        self.conn.commit()

    def delete_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item, "values")
            img = self.cursor.execute(IMAGE_WITH_ID(self.cate, item[0])).fetchone()
            os.remove(img[0])
            self.cursor.execute(DELETE_ROW(self.cate, item[0]))
            self.conn.commit()
            self.loadCate(self.cate)
    
    def update_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            itemID = self.tree.item(selected_item, "values")[0]
            item = self.cursor.execute(TEXT_SELECTION_QUERY(self.cate, itemID)).fetchone()

            def update():
                if text_entry.get() == "" or img_link.get() == "":
                    messagebox.showerror("bad entry", "both fields are required")
                    return  
                text = text_entry.get()

                ext = img_link.get().split(".")[-1]
                filename = IMAGES_DIR + RANDOM_NAME() + "." + ext

                try:
                    os.remove(item[2])
                    img_data = requests.get(img_link.get()).content
                    with open(filename, "wb") as file:
                        file.write(img_data)
                    self.cursor.execute(UPDATE_ROW(self.cate), (text, filename, item[0], ))
                    self.conn.commit()
                except Exception as e:
                    raise(e)

            root = tk.Toplevel(self)

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
                fname = self.cursor.execute(IMAGE_WITH_ID(self.cate, i)).fetchone()
                os.remove(fname[0])
                self.cursor.execute(DELETE_ROW(self.cate, i))
            print("removed old")
            try:
                self.conn.commit()
                self.conn.close()
            except Exception as e:
                print(e)

    def export(self):
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
            self.cursor.execute(CREATE_TABLE(cat))
            self.conn.commit()
            root.destroy()
            self.quit()

        tk.Button(root, text="create", command=create).pack(fill="both", padx=10, pady=10)
    
    def deleteCategory(self):
        if self.cate is not None:
            res = messagebox.askyesno(f"Delete '{self.cate}'", f"are you sure to delete '{self.cate}'")
            if res:
                try:
                    list_imgs = self.cursor.execute(ALL_IMAGE(self.cate)).fetchall()
                    for img in list_imgs:   os.remove(img[0])
                    self.cursor.execute(DROP_TABLE(self.cate))
                    self.conn.commit()
                    self.quit()
                except Exception as e:
                    print(e)

    def opencollector(self):
        Collector(self.cursor, self.conn)