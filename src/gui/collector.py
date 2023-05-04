import tkinter as tk
from tkinter import ttk
import random
import requests
from src.constants import *

class Collector(tk.Tk):
    """A class for creating a scrollable frame for data collection and database insertion."""

    def __init__(self, category, cursor, conn):
        """
        Initialize the Collector object.

        Args:
            category (str): The category for data collection.
            cursor: The cursor object for database operations.
            conn: The connection object for database operations.
        """
        super().__init__()
        self.cursor = cursor
        self.conn = conn
        self.category = category
        self.button_entry = []

        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface with a scrollable frame and control buttons.
        """
        self.title("Scrollable Frame")
        self.geometry("900x600")
        self.resizable(0, 0)

        self.create_scrollable_frame()
        self.create_control_buttons()

        self.mainloop()

    def create_scrollable_frame(self):
        """
        Create a scrollable frame with a canvas and a frame within the canvas.
        """
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

    def create_control_buttons(self):
        """
        Create control buttons in a label frame at the bottom of the window.
        """
        cont = tk.LabelFrame(self, text="Control")
        cont.pack(fill="both", padx=10, pady=10, side="bottom")

        tk.Button(cont, text="Raw", command=self.add_raw).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(cont, text="Add", command=self.add_to_db).grid(row=0, column=1, padx=10, pady=10)

    def filter_text(self):
        """
        Filter the button_entry list based on user input in the entry fields.

        Returns:
            list: A list of fetchable data (dictionaries).
        """
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
        """
        Copy the given text to the clipboard.

        Args:
            text (str): The text to be copied.
        """
        self.clipboard_clear()
        self.clipboard_append(text)

    def add_raw(self):
        """
        Create a window for entering raw text and generate buttons and entry fields.

        The entered raw text will be split into lines, and each line will correspond to a button and an entry field.
        Clicking a button will copy its corresponding text to the clipboard.
        """
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
            """
            Get the raw text from the text widget and generate buttons and entry fields based on the text.

            Each line of the raw text will correspond to a button and an entry field in the main frame.
            """
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
        """
        Add the filtered data to the database.

        The filtered data (fetchable) will be iterated, and for each item:
        - The text and image URL will be extracted.
        - An image ID will be generated.
        - The image data will be retrieved from the URL and stored in a file.
        - An SQL INSERT statement will be executed to insert the text, image filename, and None value into the database.
        """
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

                query = f"INSERT INTO {self.category} VALUES (?, ?, ?)"
                self.cursor.execute(query, (None, text, filename))
                self.conn.commit()

            except requests.exceptions.RequestException as e:
                print("Error: Failed to download image:", e)
            except Exception as e:
                print("Error:", e)