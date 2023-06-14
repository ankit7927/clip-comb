import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from src.constants import *
from src.collector import Collector
from src.creater import create
import threading, sys


class HomeUI:
    cate:str = None
    backpath:str = None
    data:list = []

    def __init__(self, tab, conn) -> None:
        self.conn = conn
        self.root = tab

        self.initUI()

    def initUI(self) -> None:
        mainframe = tk.Frame(self.root)
        mainframe.pack(fill=tk.BOTH, side=tk.LEFT)
        self.tree = ttk.Treeview(mainframe, show="headings", selectmode="browse", columns=("id", "text"), height=11)
        self.tree.pack(fill=tk.BOTH, padx=10, pady=10)

        self.tree.column("id", width=40, stretch=False, minwidth=40)
        self.tree.column("text", width=600, stretch=False, minwidth=100)
        self.tree.heading("id", text="Id")
        self.tree.heading("text", text="Texts")

        titleframe = tk.LabelFrame(mainframe, text="Title")
        titleframe.pack(padx=10, pady=5, fill=tk.X)

        def switch_callback():
            if self.random_var.get():  
                titleEntry.configure(state="disabled") 
            else:   
                titleEntry.configure(state="normal") 

        self.random_var = tk.BooleanVar(value=False)
        tk.Checkbutton(titleframe, text="Random Title", variable=self.random_var, command=switch_callback).pack(padx=5, pady=5, anchor="w")

        titles = self.conn.execute(TEXT_IMAGE_FROM_CATEGORY("titles")).fetchall()
        self.title_str = tk.StringVar(self.root)

        titleEntry = ttk.Combobox(titleframe, textvariable=self.title_str)
        titleEntry.pack(padx=10, pady=10, fill=tk.X)

        titleEntry["values"] = titles
        
        textframe = tk.LabelFrame(mainframe, text="Text")
        textframe.pack(padx=10, pady=5, fill=tk.X)

        tk.Label(textframe, text="Enter text id with ',' saparated.").pack(padx=5, pady=5, anchor=tk.W)

        text_selection = [i for i in range(1, 15)]
        self.text_ids = ttk.Combobox(textframe, values=text_selection, width=40)
        self.text_ids.current(0)
        self.text_ids.pack(padx=10, pady=10, fill=tk.X)
        
        buttonframe = tk.Frame(self.root)
        buttonframe.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        categories =  self.getCategory()
        category_var = tk.StringVar()
        category_var.set("Category")
        category_menu = tk.OptionMenu(buttonframe, category_var, command=lambda e:self.loadCate(e), *categories)
        category_menu.config(width=15)
        category_menu.pack(padx=5, pady=4, fill=tk.X)

        tk.Button(buttonframe, text="Delete Text", command=self.delete_item).pack(padx=5, pady=4, fill=tk.X)

        tk.Button(buttonframe, text="Update Text", command=self.update_item).pack(padx=5, pady=4, fill=tk.X)


        tk.Button(buttonframe, text="Collector", command=lambda: Collector(self.conn)).pack(padx=5, pady=20, fill=tk.X)


        tk.Button(buttonframe, text="New Category", command=self.addCategory).pack(padx=5, pady=4, fill=tk.X)

        tk.Button(buttonframe, text="Delete Category", command=self.deleteCategory).pack(padx=5, pady=4, fill=tk.X)

        tk.Label(buttonframe, text="").pack(pady=20)

        def change_orint(temp):
            self.template = temp

        orientations = ("vertical", "horizontal")
        self.orientation = tk.StringVar()
        self.orientation.set(orientations[0])
        video_ori = tk.OptionMenu(buttonframe, self.orientation, command=lambda e:change_orint(e), *orientations)
        video_ori.config(width=15)
        video_ori.pack(padx=5, pady=5, fill=tk.X)

        backBtn = tk.Button(buttonframe, text="Background", command=lambda:self.select_media(type="back"))
        backBtn.pack(padx=5, pady=5, fill=tk.X)

        createBtn = tk.Button(buttonframe, text="Start Creating", command=self.prepareData)
        createBtn.pack(padx=5, pady=30, fill=tk.X)

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

    def select_media(self, type):
        if type == "back":
            filetypes = (VIDEO_FILE_TUP, ALL_FILES_TUP)
            self.backpath = filedialog.askopenfilename(title="Select Background", filetypes=filetypes)
        elif type == "title":
            filetypes = (IMAGE_FILE_TUP, ALL_FILES_TUP)
            self.titlepath = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)
        else:
            raise NotImplementedError(f"Unsupported media type: {type}")



    def prepareData(self):
        if self.cate == None:
            messagebox.showerror("Bad Selection", "Category is required")
            return
        elif self.backpath == None:
            messagebox.showerror("Bad Selection", "Background is required")
            return

        raw_title = self.title_str.get()
        if raw_title == "" and not self.random_var:
            messagebox.showerror("Bad entry", "Title is required")
            return
        elif self.random_var:
            temp = self.conn.execute(RANDOM_TITLE).fetchone()
            title = temp[0]
            imglink = temp[1]
        else:
            raw_title = raw_title.split("} ")
            title = raw_title[0].replace("{", '')
            imglink = raw_title[1]

        self.data.clear()

        self.data.append({"text":title, "image":imglink})

        if self.text_ids.get() == "":
            messagebox.showerror("Bad entry", "Text ids required")
            return
        text_ids = self.text_ids.get().split(",")

        for i in text_ids:
            try:
                rec = self.conn.execute(TEXT_SELECTION_QUERY(self.cate), (i, )).fetchone()
                self.data.append({"text":rec[1], "image":rec[2]})
            except Exception as e:  raise Exception(e)

        thread = threading.Thread(target=create, args=(self.data, self.backpath, self.orientation))
        thread.start()

        self.title_str.delete(0, tk.END)
        self.backpath = None