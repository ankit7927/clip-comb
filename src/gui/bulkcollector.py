import tkinter as tk
from tkinter import ttk
import random
import requests
from src.constants import *

class BulkCollector(tk.Tk):
    category = None
    button_entry = []

    def __init__(self, category, cursor, conn) -> None:
        super().__init__()
        self.cursor = cursor
        self.conn = conn

        self.category = category

        self.setup_ui()

    def setup_ui(self):
        self.title("Scrollable Frame")
        self.geometry("900x600") 
        self.resizable(0,0)

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

        tk.Button(cont, text="Raw", command=self.add_raw).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(cont, text="Add", command=self.add_to_db).grid(row=0, column=1, padx=10, pady=10)

        self.mainloop()

    def filter_text(self):
        fetchable = []
        processed_entries = []

        for inx, btn_ent in enumerate(self.button_entry):
            if btn_ent[1].get() != "":
                fetchable.append({"text": btn_ent[2], "img": btn_ent[1].get()})
                processed_entries.append(inx)
                btn_ent[0].configure(state="disabled")
                btn_ent[1].configure(state="disabled")

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
        t = tk.Text(top, width=60, height=30, wrap=tk.NONE,
                    xscrollcommand=hscroll.set,
                    yscrollcommand=vscroll.set)
        t.pack(fill=tk.X)
        hscroll.config(command=t.xview)
        vscroll.config(command=t.yview)

        def get_raw():
            text_list = [text for text in t.get(1.0, tk.END).split("\n")]
            self.button_entry.clear()
            for inx, d in enumerate(text_list):
                btn = tk.Button(self.frame, text=d, width=70, command=lambda d=d: self.copy_to_clip(d))
                btn.grid(row=inx, column=0, padx=5, pady=10)

                ent = tk.Entry(self.frame, width=32)
                ent.grid(row=inx, column=1, padx=10, pady=10)

                self.button_entry.append((btn, ent, d))
            top.destroy()
        tk.Button(top, text="Add", command=get_raw).pack(side=tk.BOTTOM, fill="x")

    def add_to_db(self):
        fetchable = self.filter_text()
        for raw_data in fetchable:
            text = raw_data["text"]
            ext = raw_data["img"].split(".")[-1]
            image_id = str(random.randint(10000000, 99999999))
            filename = IMAGES_DIR + image_id + "." + ext

            try:
                img_data = requests.get(raw_data["img"]).content
                with open(filename, "wb") as file:
                    file.write(img_data)

                self.cursor.execute(f"INSERT INTO {self.category} VALUES(?, ?, ?)", (None, text, filename,))
                self.conn.commit()
            except Exception as e:
                print("exception : ", e)
                continue