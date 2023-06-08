import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from src.constants import *
from src.collector import Collector
from src.creater import create
import threading


class HomeUI:
    titlepath:str = None
    cate:str = None
    backpath:str = None
    vert:bool = True
    title:bool = True
    data:list = []
    removable:list = []

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
            if switch_var.get() == 1: 
                self.title = True
                self.titleEntry.configure(state="normal") 
                imageBtn.configure(state="normal")
            else:   
                self.title = False
                self.titleEntry.configure(state="disabled") 
                imageBtn.configure(state="disabled")

        switch_var = tk.IntVar()
        switch_var.set(1)
        tk.Checkbutton(titleframe, text="Include Title", variable=switch_var, command=switch_callback).grid(padx=5, pady=5, row=0, sticky="w")

        self.titleEntry = tk.Entry(titleframe, width=80)
        self.titleEntry.grid(padx=10, pady=5, row=1, column=0)

        imageBtn = tk.Button(titleframe, text="Title Image", command=lambda:self.select_media(type="title"))
        imageBtn.grid(padx=5, pady=5, row=1, column=1)
        

        textframe = tk.LabelFrame(mainframe, text="Text")
        textframe.pack(padx=10, pady=5, fill=tk.X)

        tk.Label(textframe, text="Select Number of text or type specific text id with ',' saparated").grid(padx=5, pady=5, row=0, sticky=tk.W)

        text_selection = [i for i in range(1, 15)]
        self.text_count_select = ttk.Combobox(textframe, values=text_selection, width=40)
        self.text_count_select.current(0)
        self.text_count_select.grid(row=1, column=0, padx=5, pady=10, sticky=tk.W)
        
        def delete_callback():
            if delete_var.get() == 1: self.delete = True 
            else:   self.delete = False

        delete_var = tk.IntVar()
        delete_var.set(1)
        tk.Checkbutton(textframe, text="Delete Texts", variable=delete_var, command=delete_callback).grid(padx=10, pady=10, row=1, column=1)





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

        def change_orint(ori):
            if ori == "Vertical" : self.vert = True
            else : self.vert = False

        tk.Label(buttonframe, text="").pack(pady=20)

        orient = ("Vertical", "Horizontal")
        orient_var = tk.StringVar()
        orient_var.set(orient[0])
        video_ori = tk.OptionMenu(buttonframe, orient_var, command=lambda e:change_orint(e), *orient)
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

    def removeOld(self):
        if self.delete:
            for i in self.removable:
                self.conn.execute(DELETE_ROW(self.cate, i))
            print("removed old")


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
        
        if self.title:
            if self.titleEntry.get() == "":
                messagebox.showerror("Bad entry", "Title is required")
                return
            elif self.titlepath == None:
                messagebox.showerror("Bad Selection", "Title image required")
                return

            self.data.append({"text":self.titleEntry.get(), "image":self.titlepath})
        
        text_sele = self.text_count_select.get().split(",")

        if len(text_sele) != 1:
            for i in text_sele:
                try:
                    rec = self.conn.execute(TEXT_SELECTION_QUERY(self.cate, i)).fetchone()
                    self.data.append({"text":rec[1], "image":rec[2]})
                except Exception as e:  print(e)
            self.removable= text_sele
        else:
            records = self.conn.execute(f"SELECT * FROM {self.cate}").fetchmany(int(self.text_count_select.get()))

            for rec in records:
                self.removable.append(rec[0])
                self.data.append({"text":rec[1], "image":rec[2]})

        thread = threading.Thread(target=create, args=(self.data, self.backpath, self.vert, self.conn, self.delete, self.cate, self.removable))
        thread.start()

        self.titlepath = None
        self.titleEntry.delete(0, tk.END)
        self.backpath = None
        self.data = []
        self.removable = []