import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
from src.constants import *
from src.creater import create
import threading


class Tab2UI:
    titlepath:str = None
    cate:str = None
    backpath:str = None
    title:bool = True
    vert:bool = True
    title:bool = True
    delete:bool = True
    data:list = []
    removable:list = []


    def getCategory(self):
        tables = self.cursor.execute(ALL_TABLE_QUERY).fetchall()
        if len(tables) == 0:
            return ["#None"]
        if tables.count((SEQUENCE_TABLE_NAME,)) > 0:
            tables.remove((SEQUENCE_TABLE_NAME,))
        return [table[0] for table in tables]
    
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
                    rec = self.cursor.execute(TEXT_SELECTION_QUERY(self.cate, i)).fetchone()
                    self.data.append({"text":rec[1], "image":rec[2]})
                except Exception as e:  print(e)
            self.removable= text_sele
        else:
            records = self.cursor.execute(f"SELECT * FROM {self.cate}").fetchmany(int(self.text_count_select.get()))

            for rec in records:
                self.removable.append(rec[0])
                self.data.append({"text":rec[1], "image":rec[2]})

        ## start new thread
        thread = threading.Thread(target=create, args=(self.data, self.backpath, self.vert, self.delete))
        thread.start()

        #reset parameters
        self.titlepath = None
        self.titleEntry.delete(0, tk.END)
        self.backpath = None
        self.data = []
        self.removable = []


    def __init__(self, tab, cursor):
        self.cursor = cursor
        self.root = tab

        self.initUI()


    def initUI(self):
        geometry = tk.LabelFrame(self.root, text="Geometry")
        geometry.pack(padx=10, pady=5, fill="x")

        categories =  self.getCategory()
        category_var = tk.StringVar()
        category_var.set("Category")

        def setcate(e): self.cate = e   

        category_menu = tk.OptionMenu(geometry, category_var, command=setcate, *categories)
        category_menu.config(width=15)
        category_menu.grid(padx=5, pady=5, row=0, column=0)

        def change_orint(ori):
            if ori == "Vertical" : self.vert = True
            else : self.vert = False

        orient = ("Vertical", "Horizontal")
        orient_var = tk.StringVar()
        orient_var.set(orient[0])
        video_ori = tk.OptionMenu(geometry, orient_var, command=lambda e:change_orint(e), *orient)
        video_ori.config(width=10)
        video_ori.grid(padx=5, pady=5, row=0, column=1)

        backBtn = tk.Button(geometry, text="Background", command=lambda:self.select_media(type="back"))
        backBtn.grid(padx=5, pady=5, row=0, column=2)


        titleframe = tk.LabelFrame(self.root, text="Title")
        titleframe.pack(padx=10, pady=5, fill="x")

        def switch_callback():
            if switch_var.get() == 1: self.title = True 
            else:   self.title = False

        switch_var = tk.IntVar()
        switch_var.set(1)
        tk.Checkbutton(titleframe, text="Include Title", variable=switch_var, command=switch_callback).grid(padx=5, pady=5, row=0, sticky="w")

        self.titleEntry = tk.Entry(titleframe, width=50)
        self.titleEntry.grid(padx=10, pady=5, row=1, column=0)

        imageBtn = tk.Button(titleframe, text="Title Image", command=lambda:self.select_media(type="title"))
        imageBtn.grid(padx=5, pady=5, row=1, column=1)
        

        textframe = tk.LabelFrame(self.root, text="Text")
        textframe.pack(padx=10, pady=5, fill="x")

        tk.Label(textframe, text="Select Number of text or type specific text id with ',' saparated").grid(padx=5, pady=5, row=0, sticky="w")

        text_selection = [i for i in range(1, 8)]
        self.text_count_select = ttk.Combobox(textframe, values=text_selection, width=40)
        self.text_count_select.current(0)
        self.text_count_select.grid(row=1, column=0, padx=5, pady=10, sticky="w")
        
        def delete_callback():
            if delete_var.get() == 1: self.delete = True 
            else:   self.delete = False

        delete_var = tk.IntVar()
        delete_var.set(1)
        tk.Checkbutton(textframe, text="Delete Texts", variable=delete_var, command=delete_callback).grid(padx=10, pady=10, row=1, column=1)

        createBtn = tk.Button(self.root, text="Start Creating", command=self.prepareData)
        createBtn.pack(padx=10, pady=10, fill="x")