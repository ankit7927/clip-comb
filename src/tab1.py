import tkinter as tk
from tkinter import ttk, messagebox
from src.constants import *
import os, random, requests


class Tab1UI:

    def getCategory(self):
        tables = self.cursor.execute(ALL_TABLE_QUERY).fetchall()
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
            texts = self.cursor.execute(TEXT_ID_FROM_CATEGORY(cate)).fetchall()
            for text in texts:
                self.tree.insert("", tk.END, values=text)

    def delete_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item, "values")
            img = self.cursor.execute(IMAGE_WITH_ID(self.cate, item[0])).fetchone()
            os.remove(img[0])
            self.cursor.execute(DELETE_ROW(self.cate, item[0]))
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
                image_id = str(random.randint(10000000, 99999999))
                filename = IMAGES_DIR + image_id + "." + ext

                try:
                    os.remove(item[2])
                    img_data = requests.get(img_link.get()).content
                    with open(filename, "wb") as file:
                        file.write(img_data)
                    self.cursor.execute(UPDATE_ROW(self.cate), (text, filename, item[0], ))
                    self.conn.commit()
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

    def __init__(self, tab, cursor):
        self.cursor = cursor
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



