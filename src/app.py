import tkinter as tk
import sqlite3
from src.constants import *
from src.hometab import HomeUI
from src.extractortab import Extractor

class ClipComb(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.set_ui()

    def set_ui(self) -> None:
        self.conn = sqlite3.connect(DB_PATH)

        self.title(APP_NAME)
        self.geometry("800x500")
        self.resizable(0, 0)

        notebook = tk.ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        tab1 = tk.ttk.Frame(notebook)
        tab2 = tk.ttk.Frame(notebook)

        notebook.add(tab1, text="Shorts")
        notebook.add(tab2, text="Extractor")

        HomeUI(tab1, self.conn)
        Extractor(tab2)

        self.mainloop()
        self.conn.commit()