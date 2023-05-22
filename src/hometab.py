import tkinter as tk
from tkinter import ttk, messagebox
from src.constants import *
import os, requests


class HomeUI:

    def getCategory(self):
        tables = self.conn.execute(ALL_TABLE_QUERY).fetchall()
        if len(tables) == 0:
            return ["#None"]
        if tables.count((SEQUENCE_TABLE_NAME,)) > 0:
            tables.remove((SEQUENCE_TABLE_NAME,))
        return [table[0] for table in tables]

    def loadCate(self, cate):
        if cate == "#None":
            return
        if cate != "":
            self.cate = cate
            for item in self.tree.get_children():
                self.tree.delete(item)
            texts = self.conn.execute(TEXT_ID_FROM_CATEGORY(cate)).fetchall()
            for text in texts:
                self.tree.insert("", tk.END, values=text)

    def delete_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item, "values")
            img = self.conn.execute(IMAGE_WITH_ID(self.cate, item[0])).fetchone()
            os.remove(img[0])
            self.conn.execute(DELETE_ROW(self.cate, item[0]))
            self.loadCate(self.cate)
    
    def update_item(self):
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

                self.conn.execute(UPDATE_ROW_TEXT, (text, item[0]))

                if image_link != "":
                    ext = img_link.get().split(".")[-1]
                    filename = IMAGES_DIR + RANDOM_NAME() + "." + ext

                    try:
                        os.remove(item[2])
                        img_data = requests.get(image_link).content
                        with open(filename, "wb") as file:
                            file.write(img_data)
                        self.conn.execute(UPDATE_ROW_IMAGE, (filename, item[0], ))
                    except Exception as e:
                        raise(e)

            root = tk.Toplevel(self.root)

            text_entry = tk.Entry(root, width=40)
            text_entry.pack(padx=10, pady=10)
            text_entry.insert(0, item[1])

            img_link = tk.Entry(root, width=40)
            img_link.pack(padx=10, pady=10)

            tk.Button(root, text="Update", command=update).pack(padx=10, pady=10)

            root.mainloop()

    def __init__(self, tab, conn):
        self.conn = conn
        self.root = tab

        self.initUI()

    def initUI(self):
        listFrame = tk.Frame(self.root)
        listFrame.pack(fill="both", pady=10, expand=True)

        self.tree = ttk.Treeview(listFrame, show="headings", selectmode="browse", columns=("id", "text"))
        self.tree.pack(padx=10, fill="both", expand=True, side=tk.LEFT)

        self.tree.column("id", width=40, stretch=False, minwidth=40)
        self.tree.heading("id", text="Id")
        self.tree.heading("text", text="Texts")

        bottomframe = tk.LabelFrame(self.root, text="Text")
        bottomframe.pack(padx=10, pady=10, fill="both", side="bottom")

        tk.Button(bottomframe, text="Delete", command=self.delete_item).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(bottomframe, text="Update", command=self.update_item).grid(row=0, column=1, padx=5, pady=5)

        categories =  self.getCategory()
        category_var = tk.StringVar()
        category_var.set("Category")
        category_menu = tk.OptionMenu(bottomframe, category_var, command=lambda e:self.loadCate(e), *categories)
        category_menu.grid(padx=5, pady=5, row=0, column=2)



