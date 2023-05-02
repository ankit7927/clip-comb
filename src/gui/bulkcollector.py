import tkinter as tk
from tkinter import ttk
import random, requests
from src.constants import *

class BulkCollector:
    category=None
    conn=None
    cursor = None
    btnent = []
    text = []

    root = None
    scrollable_frame = None
    
    def __init__(self, category, cursor, conn) -> None:
        self.category = category
        self.cursor = cursor
        self.conn = conn

        self.root = tk.Tk()
        self.root.title(f"Bulk Collector for {self.category}")
        container = ttk.Frame(self.root)
        container.pack()

        canvas = tk.Canvas(container, width=800, height=500)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        cont= tk.LabelFrame(self.root, text="control")
        cont.pack(fill="both", padx=10, pady=10)

        tk.Button(cont, text="raw", command=lambda: self.add_raw()).grid(row=0,column=0, padx=10, pady=10)
        tk.Button(cont, text="add",command=self.addToDB).grid(row=0,column=1, padx=10, pady=10)

        self.root.mainloop()


    def filterText(self):
        fatchable = []
        for i in range(len(self.btnent)):
            if self.btnent[i][1].get() != "":
                fatchable.append({"text":self.text[i], "img":self.btnent[i][1].get()})
                self.btnent[i][0].grid_forget()
                self.btnent[i][1].grid_forget()

        return fatchable


    def copytoClip(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)


    def add_raw(self):
        top = tk.Toplevel(self.root)
        h = tk.Scrollbar(top, orient = 'horizontal')
        h.pack(fill = "x")
        v = tk.Scrollbar(top)
        v.pack(side = tk.RIGHT, fill = "y")
        t = tk.Text(top, width = 60, height = 30, wrap = tk.NONE,
                    xscrollcommand = h.set,
                    yscrollcommand = v.set)
        t.pack(fill=tk.X)
        h.config(command=t.xview)
        v.config(command=t.yview)

        def getRaw():
            self.text = [text for text in t.get(1.0, tk.END).split("\n")]

            for inx, d in enumerate(self.text):
                btn = tk.Button(self.scrollable_frame, text=d, width=60, command=lambda d=d: self.copytoClip(d))
                btn.grid(row=inx, column=0, padx=5, pady=10)

                ent = tk.Entry(self.scrollable_frame, width=30)
                ent.grid(row=inx, column=1, padx=10, pady=10)

                self.btnent.append((btn, ent))
            
            top.destroy()
        
        tk.Button(top, text="add", command=getRaw).pack(side = tk.BOTTOM)

        top.mainloop()
    

    def addToDB(self):
        fatchable = self.filterText()
        for inx, rawData in enumerate(fatchable):
            text = rawData["text"]
            ext = rawData["img"].split(".")[-1]
            imageid = str(random.randint(10000000, 99999999))
            filename = IMAGES_DIR+imageid+"."+ext

            imgdata = requests.get(rawData["img"]).content
            with open(filename, "wb") as file:
                file.write(imgdata)
            
            self.cursor.execute(f"INSERT INTO {self.category} VALUES(?, ?, ?)", (None, text, filename, ))
        self.conn.commit()