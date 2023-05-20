import tkinter as tk
from tkinter import ttk
import random
import requests
from src.constants import *

class Collector(tk.Tk):
    cate:str = None
    def __init__(self, cursor, conn):
        super().__init__()
        self.cursor = cursor
        self.conn = conn
        self.button_entry = []

        self.setup_ui()

    def setup_ui(self):
        self.title("Raw Text Collector")
        self.geometry("900x600")
        self.resizable(0, 0)        

        cframe = tk.Frame(self)
        cframe.pack(fill="both", expand=True)

        canvas = tk.Canvas(cframe)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(cframe, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        self.frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        cont = tk.LabelFrame(self, text="Control")
        cont.pack(fill="both", padx=10, pady=10, side="bottom")

        def loadCate(cate):
            self.cate = cate

        categories =  self.getCategory()
        category_var = tk.StringVar()
        category_var.set("Category")
        category_menu = tk.OptionMenu(cont, category_var, command=lambda e:loadCate(e), *categories)
        category_menu.grid(padx=10, pady=10, row=0, column=0)

        tk.Button(cont, text="Raw", command=self.add_raw).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(cont, text="Add", command=self.add_to_db).grid(row=0, column=2, padx=10, pady=10)

        self.mainloop()


    def getCategory(self):
        tables = self.cursor.execute(ALL_TABLE_QUERY).fetchall()
        if len(tables) == 0:
            return ["#None"]
        if tables.count((SEQUENCE_TABLE_NAME,)) > 0:
            tables.remove((SEQUENCE_TABLE_NAME,))
        return [table[0] for table in tables]

    def filter_text(self):
        fetchable = []
        processed_entries = []

        for index, (button, entry, text) in enumerate(self.button_entry):
            if entry.get():
                fetchable.append({"text": text, "img": entry.get()})
                processed_entries.append(index)
                button.configure(state="disabled")
                entry.configure(state="disabled")

        self.button_entry = [entry for index, entry in enumerate(self.button_entry) if index not in processed_entries]

        return fetchable

    def copy_to_clip(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)

    def add_raw(self):
        top = tk.Toplevel(self)
        hscroll = tk.Scrollbar(top, orient='horizontal')
        hscroll.pack(fill="x")
        vscroll = tk.Scrollbar(top)
        vscroll.pack(side=tk.RIGHT, fill="y")
        t = tk.Text(top, width=80, height=30, wrap=tk.NONE,
                    xscrollcommand=hscroll.set,
                    yscrollcommand=vscroll.set)
        t.pack(fill=tk.X)
        hscroll.config(command=t.xview)
        vscroll.config(command=t.yview)

        def get_raw():
            text_list = [text for text in t.get(1.0, tk.END).split("\n")]
            self.button_entry.clear()
            for inx, d in enumerate(text_list):
                tempFrame = tk.Frame(self.frame)
                tempFrame.pack(padx=10, pady=10, expand=True)

                btn = tk.Button(tempFrame, text=d, command=lambda d=d: self.copy_to_clip(d), width=100)
                btn.pack(padx=10, pady=5)

                ent = tk.Entry(tempFrame)
                ent.pack(padx=10, pady=5, fill="x")

                self.button_entry.append((btn, ent, d))
            top.destroy()
        tk.Button(top, text="Add", command=get_raw).pack(side=tk.BOTTOM, fill="x")

    def add_to_db(self):
        fetchable = self.filter_text()

        for data in fetchable:
            text = data["text"]
            image_url = data["img"]
            ext = image_url.split(".")[-1]
            image_id = str(random.randint(10000000, 99999999))
            filename = IMAGES_DIR + image_id + "." + ext

            try:
                response = requests.get(image_url)
                response.raise_for_status()

                with open(filename, "wb") as file:
                    file.write(response.content)

                self.cursor.execute(INSERT_TEXT_IMAGE(self.cate), (None, text, filename))
                self.conn.commit()

            except requests.exceptions.RequestException as e:
                print("Error: Failed to download image:", e)
            except Exception as e:
                print("Error:", e)