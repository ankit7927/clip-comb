import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
from src.constants import *
from src.creater import create
import threading


class CreatorUI:
    
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
        tables = self.conn.execute(ALL_TABLE_QUERY).fetchall()
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


    def __init__(self, tab, conn):
        self.conn = conn
        self.root = tab

        self.initUI()


    def initUI(self):
        geometry = tk.Frame(self.root)
        geometry.pack(fill=tk.BOTH, side=tk.RIGHT)

        categories =  self.getCategory()
        category_var = tk.StringVar()
        category_var.set("Category")

        def setcate(e): self.cate = e   

        category_menu = tk.OptionMenu(geometry, category_var, command=setcate, *categories)
        category_menu.config(width=15)
        category_menu.pack(padx=5, pady=5, fill=tk.X)

        def change_orint(ori):
            if ori == "Vertical" : self.vert = True
            else : self.vert = False

        orient = ("Vertical", "Horizontal")
        orient_var = tk.StringVar()
        orient_var.set(orient[0])
        video_ori = tk.OptionMenu(geometry, orient_var, command=lambda e:change_orint(e), *orient)
        video_ori.config(width=15)
        video_ori.pack(padx=5, pady=5, fill=tk.X)

        backBtn = tk.Button(geometry, text="Background", command=lambda:self.select_media(type="back"))
        backBtn.pack(padx=5, pady=5, fill=tk.X)

        createBtn = tk.Button(geometry, text="Start Creating", command=self.prepareData)
        createBtn.pack(padx=5, pady=30, fill=tk.X)


        testframe = tk.Frame(self.root)
        testframe.pack(fill="both", expand=True, side=tk.LEFT)


        titleframe = tk.LabelFrame(testframe, text="Title")
        titleframe.pack(padx=10, pady=5, fill=tk.X)

        def switch_callback():
            if switch_var.get() == 1: self.title = True 
            else:   self.title = False

        switch_var = tk.IntVar()
        switch_var.set(1)
        tk.Checkbutton(titleframe, text="Include Title", variable=switch_var, command=switch_callback).grid(padx=5, pady=5, row=0, sticky="w")

        self.titleEntry = tk.Entry(titleframe, width=80)
        self.titleEntry.grid(padx=10, pady=5, row=1, column=0)

        imageBtn = tk.Button(titleframe, text="Title Image", command=lambda:self.select_media(type="title"))
        imageBtn.grid(padx=5, pady=5, row=1, column=1)
        

        textframe = tk.LabelFrame(testframe, text="Text")
        textframe.pack(padx=10, pady=5, fill=tk.X)

        tk.Label(textframe, text="Select Number of text or type specific text id with ',' saparated").grid(padx=5, pady=5, row=0, sticky=tk.W)

        text_selection = [i for i in range(1, 8)]
        self.text_count_select = ttk.Combobox(textframe, values=text_selection, width=40)
        self.text_count_select.current(0)
        self.text_count_select.grid(row=1, column=0, padx=5, pady=10, sticky=tk.W)
        
        def delete_callback():
            if delete_var.get() == 1: self.delete = True 
            else:   self.delete = False

        delete_var = tk.IntVar()
        delete_var.set(1)
        tk.Checkbutton(textframe, text="Delete Texts", variable=delete_var, command=delete_callback).grid(padx=10, pady=10, row=1, column=1)

        