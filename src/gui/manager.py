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

        self.title(APP_NAME)
        self.resizable(0, 0)

        menubar = tk.Menu(self)

        cate_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Category", menu=cate_menu)

        cate_menu.add_command(label="New", command=self.addCategory)
        cate_menu.add_command(label="Delete", command=self.deleteCategory)
        cate_menu.add_separator()
        cate_menu.add_command(label="Import", command=self.import_db)
        cate_menu.add_command(label="Export", command=self.export)

        manager_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_command(label="Collector", command=self.opencollector)

        self.config(menu=menubar)

        middleFrame = tk.LabelFrame(self, text="Creation")
        middleFrame.pack(padx=10, pady=5, fill="both")

        categories =  self.getCategory()
        category_var = tk.StringVar(self)
        category_var.set("Category")

        category_menu = tk.OptionMenu(middleFrame, category_var, command=lambda e:self.loadCate(e), *categories)
        category_menu.config(width=15)
        category_menu.grid(padx=5, pady=5, row=0, column=0)

        orient = ("Vertical", "Horizontal")
        orient_var = tk.StringVar(self)
        orient_var.set(orient[0])
        video_ori = tk.OptionMenu(middleFrame, orient_var, *orient)
        video_ori.config(width=10)
        video_ori.grid(padx=5, pady=5, row=0, column=1)

        fonts = os.listdir(FONTS_DIR)
        self.font_var = tk.StringVar(self)
        self.font_var.set(fonts[1])
        font_select = tk.OptionMenu(middleFrame, self.font_var, *fonts)
        font_select.config(width=15)
        font_select.grid(row=0, column=2, padx=5, pady=5)

        def switch_callback():
            if switch_var.get() == 1: self.heading = True 
            else:   self.heading = False

        switch_var = tk.IntVar()
        switch_var.set(1)
        switch = tk.Checkbutton(middleFrame, text="Include Title", variable=switch_var, command=switch_callback)
        switch.grid(padx=5, pady=5, row=0, column=3)

        self.titleEntry = tk.Entry(middleFrame, width=77)
        self.titleEntry.grid(padx=10, pady=5, row=1, column=0, columnspan=4)

        imageBtn = tk.Button(middleFrame, text="Title Image", command=lambda:self.select_media(type="title"), width=15)
        imageBtn.grid(padx=5, pady=5, row=2, column=0)

        backBtn = tk.Button(middleFrame, text="Background", command=lambda:self.select_media(type="back"), width=15)
        backBtn.grid(padx=5, pady=5, row=2, column=1)

        text_selection = [i for i in range(1, 8)]
        self.text_count_select = ttk.Combobox(middleFrame, values=text_selection, width=15)
        self.text_count_select.current(0)
        self.text_count_select.grid(row=2, column=2, padx=5, pady=5)

        createBtn = tk.Button(middleFrame, text="Start Creating", command=self.create, width=15)
        createBtn.grid(padx=5, pady=5, row=2, column=3)


        listFrame = tk.Frame(self)
        listFrame.pack(fill="both")

        self.tree = ttk.Treeview(listFrame, show="headings", selectmode="browse", columns=("id", "text"), height=15)
        self.tree.pack(padx=10, fill="both", expand=True, side=tk.LEFT)

        self.tree.column("id", width=40, stretch=False, minwidth=40)
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
            filetypes = (VIDEO_FILE_TUP, ALL_FILES_TUP)
            self.backPath = filedialog.askopenfilename(title="Select Background", filetypes=filetypes)
        elif type == "title":
            filetypes = (IMAGE_FILE_TUP, ALL_FILES_TUP)
            self.titlePath = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)
        else:
            raise NotImplementedError(f"Unsupported media type: {type}")

    def getCategory(self):
        """
        Retrieve the list of available categories from the database.

        Returns:
            list: A list of category names.
        """
        tables = self.cursor.execute(ALL_TABLE_QUERY).fetchall()
        if len(tables) == 0:
            return ["#None"]
        if tables.count((SEQUENCE_TABLE_NAME,)) > 0:
            tables.remove((SEQUENCE_TABLE_NAME,))
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
            texts = self.cursor.execute(TEXT_ID_FROM_CATEGORY(cate)).fetchall()
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

        self.font = self.font_var.get()

        text_sele = self.text_count_select.get().split(",")

        if len(text_sele) != 1:
            for i in text_sele:
                try:
                    rec = self.cursor.execute(f"").fetchone()
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
            img = self.cursor.execute(IMAGE_WITH_ID(self.cate, item[0])).fetchone()
            os.remove(img[0])
            self.cursor.execute(DELETE_ROW(self.cate, item[0]))
            self.conn.commit()
            self.loadCate(self.cate)
    
    def update_item(self):
        """
        Update the selected item in the tree view and database.
        """
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
        """
        Export the SQLite database as a ZIP archive.
        """
        make_archive(ZIP_NAME, base_dir=DB_DIR, format="zip", root_dir=".")

    def import_db(self):
        
        """
        Import a SQLite database from a ZIP archive.
        """
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
        if self.cate is not None:
            Collector(self.cate, self.cursor, self.conn)
        