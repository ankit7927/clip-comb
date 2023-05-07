import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
import sqlite3, os, random, requests, shutil, sys
from src.constants import *
from shutil import make_archive, unpack_archive
from src.gui.collector import Collector

class Manager(tk.Tk):
    """
    The Manager class represents the main application window for the Shorts Maker.

    It allows the user to create shorts by selecting a category, providing title information, selecting media files,
    and managing the texts associated with the selected category.
    """
    data: list = []
    backPath: str = None
    font: str = None

    removable: list = []

    conn: sqlite3.Connection = None
    cursor: sqlite3.Cursor = None

    cate: str = None
    heading:bool = True

    def __init__(self) -> None:
        super().__init__()
        self.set_ui()

    def set_ui(self) -> None:
        """
        Set up the user interface of the application.
        """
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        self.title("Shorts Maker")
        self.resizable(0, 0)

        menubar = tk.Menu(self)

        cate_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="category", menu=cate_menu)

        cate_menu.add_command(label="New", command=self.addCategory)
        cate_menu.add_command(label="Delete", command=self.deleteCategory)
        cate_menu.add_separator()
        cate_menu.add_command(label="Import", command=self.import_db)
        cate_menu.add_command(label="Export", command=self.export)

        manager_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_command(label="collector", command=self.opencollector)

        manager_menu.add_command(label="Collector")

        self.config(menu=menubar)

        middleFrame = tk.LabelFrame(self, text="Creation")
        middleFrame.pack(padx=10, pady=10, fill="both")

        options =  self.getCategory()
        option_var = tk.StringVar(self)
        option_var.set("Category")

        option_menu = tk.OptionMenu(middleFrame, option_var, command=lambda e:self.loadCate(e), *options)
        option_menu.grid(padx=5, pady=10, row=0, column=0)

        self.titleEntry = tk.Entry(middleFrame, width=77)
        self.titleEntry.grid(padx=5, pady=10, row=0, column=1, columnspan=5)

        imageBtn = tk.Button(middleFrame, text="Title Image", command=lambda:self.select_media(type="title"))
        imageBtn.grid(padx=5, pady=10, row=1, column=0)

        backBtn = tk.Button(middleFrame, text="Background", command=lambda:self.select_media(type="back"))
        backBtn.grid(padx=5, pady=10, row=1, column=1)

        fonts = os.listdir(FONTS_DIR)
        self.font_select = ttk.Combobox(middleFrame, values=fonts, width=20)
        self.font_select.current(0)
        self.font_select.grid(row=1, column=2, padx=5, pady=5)

        text_selection = [i for i in range(1, 8)]
        self.text_count_select = ttk.Combobox(middleFrame, values=text_selection, width=8)
        self.text_count_select.current(0)
        self.text_count_select.grid(row=1, column=3, padx=5, pady=5)

        def switch_callback():
            if switch_var.get() == 1: self.heading = True 
            else:   self.heading = False 

        switch_var = tk.IntVar()
        switch_var.set(1)
        switch = tk.Checkbutton(middleFrame, text="Include Title", variable=switch_var, command=switch_callback)
        switch.grid(padx=5, pady=5, row=1, column=4)

        createBtn = tk.Button(middleFrame, text="Start Creating", command=self.create)
        createBtn.grid(padx=5, pady=5, row=1, column=5)


        listFrame = tk.Frame(self)
        listFrame.pack(fill="both")

        self.tree = ttk.Treeview(listFrame, show="headings", selectmode="browse", columns=("id", "text"), height=15)
        self.tree.pack(padx=10, fill="both", expand=True, side=tk.LEFT)

        self.tree.column("id", width=30, stretch=False, minwidth=30)
        self.tree.heading("id", text="Id")

        bottomframe = tk.LabelFrame(self, text="Text")
        bottomframe.pack(padx=10, pady=10, fill="both")

        tk.Button(bottomframe, text="Delete", command=self.delete_item).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(bottomframe, text="Update", command=self.update_item).grid(row=0, column=1, padx=5, pady=5)

        self.mainloop()
        self.conn.commit()
        

        
    def select_media(self, type):
        """
        Open a file dialog to select media files for title or background.

        Args:
            type (str): The type of media file to select ('title' or 'back').

        Raises:
            NotImplementedError: If the media file type is not supported.
        """
        if type == "back":
            filetypes = (("Video file", "*.mp4"), ("All files", "*.*"))
            self.backPath = filedialog.askopenfilename(title="Select Background", filetypes=filetypes)
        elif type == "title":
            filetypes = (("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*"))
            self.titlePath = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)
        else:
            raise NotImplementedError(f"Unsupported media type: {type}")

    def getCategory(self):
        """
        Retrieve the list of available categories from the database.

        Returns:
            list: A list of category names.
        """
        tables = self.cursor.execute("select name from sqlite_master where type='table';").fetchall()
        if len(tables) == 0:
            return ["#None"]
        if tables.count(('sqlite_sequence',)) > 0:
            tables.remove(('sqlite_sequence',))
        return [table[0] for table in tables]

    def loadCate(self, cate):
        """
        Load and display the texts associated with the selected category.

        Args:
            cate (str): The name of the selected category.
        """
        if cate == "#None":
            return
        self.cate = cate
        if cate != "":
            self.tree.heading("text", text=cate)
            for item in self.tree.get_children():
                self.tree.delete(item)
            texts = self.cursor.execute(f"select id, text from {cate};").fetchall()
            for text in texts:
                self.tree.insert("", tk.END, values=text)

    def create(self):
        """
        Create a new short with the selected category, title, media files, and texts.
        """
        if self.cate == None:
            messagebox.showerror("Bad Selection", "Category is required")
            return
        elif self.backPath == None:
            messagebox.showerror("Bad Selection", "Background is required")
            return

        if self.heading:
            if self.titleEntry.get() == "":
                messagebox.showerror("Bad entry", "Title is required")
                return
            elif self.titlePath == None:
                messagebox.showerror("Bad Selection", "Title image required")
                return

            self.data.insert(0, {"text":self.titleEntry.get(), "image":self.titlePath})

        self.font = self.font_select.get()

        text_sele = self.text_count_select.get().split(",")

        if len(text_sele) != 1:
            for i in text_sele:
                try:
                    rec = self.cursor.execute(f"SELECT * FROM {self.cate} WHERE id={i}").fetchone()
                    self.data.append({"text":rec[1], "image":rec[2]})
                except Exception as e:  print(e)
            self.removable= text_sele
        else:
            records = self.cursor.execute(f"SELECT * FROM {self.cate}").fetchmany(int(self.text_count_select.get()))

            for rec in records:
                self.removable.append(rec[0])
                self.data.append({"text":rec[1], "image":rec[2]})

        self.destroy()

    def get(self):
        """
        Get the created short, background path, and selected font.

        Returns:
            tuple: A tuple containing the created short, background path, and selected font.
        """
        if len(self.data) == 0: sys.exit(0)
        return (self.data, self.backPath, self.font)

    def delete_item(self):
        """
        Delete the selected item from the tree view and database.
        """
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item, "values")
            img = self.cursor.execute(f"SELECT image from {self.cate} WHERE id={item[0]}").fetchone()
            os.remove(img[0])
            self.cursor.execute(f"DELETE FROM {self.cate} WHERE id={item[0]}")
            self.conn.commit()
            self.loadCate(self.cate)
    
    def update_item(self):
        """
        Update the selected item in the tree view and database.
        """
        selected_item = self.tree.selection()
        if selected_item:
            itemID = self.tree.item(selected_item, "values")[0]
            item = self.cursor.execute(f"SELECT * from {self.cate} WHERE id={itemID}").fetchone()

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
                    self.cursor.execute(f"UPDATE {self.cate} SET text=?, image=? WHERE id={item[0]}", (text, filename, ))
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
        """
        Remove the old texts and associated images from the database
        """
        for i in self.removable:
            fname = self.cursor.execute(f"SELECT image FROM {self.cate} WHERE id={i}").fetchone()
            os.remove(fname[0])
            self.cursor.execute(f"DELETE FROM {self.cate} WHERE id={i}")
        print("removed old")
        try:
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            print(e)

    def export(self):
        """
        Export the SQLite database as a ZIP archive.
        """
        make_archive(ZIP_NAME, base_dir=DB_DIR, format="zip", root_dir=".")

    def import_db(self):
        
        """
        Import a SQLite database from a ZIP archive.
        """
        filetypes = (("Archive file", "*.zip"), ("All files", "*.*"))
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
            self.cursor.execute(f"create table {cat} (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, image TEXT)")
            self.conn.commit()
            root.destroy()
            self.quit()

        tk.Button(root, text="create", command=create).pack(fill="both", padx=10, pady=10)

    
    def deleteCategory(self):
        if self.cate is not None:
            res = messagebox.askyesno(f"Delete '{self.cate}'", f"are you sure to delete '{self.cate}'")
            if res:
                try:
                    list_imgs = self.cursor.execute(f"SELECT image from {self.cate}").fetchall()
                    for img in list_imgs:   os.remove(img[0])
                    self.cursor.execute(f"DROP TABLE {self.cate}")
                    self.conn.commit()
                    self.quit()
                except Exception as e:
                    print(e)

    def opencollector(self):
        if self.cate is not None:
            Collector(self.cate, self.cursor, self.conn)
        