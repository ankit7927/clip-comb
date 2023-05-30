import tkinter as tk
from tkinter import filedialog, messagebox
from src.creater import extract
from src.constants import *
import threading

class Extractor:

    video_file:str = ""
    music_file:str = ""

    def delete_one(self):
        selected = self.durTree.focus()
        if selected != "":
            self.durTree.delete(selected)

    def delete_all(self):
        all_durs = self.durTree.get_children()
        for i in all_durs:
                self.durTree.delete(i)
        
    def saveDur(self):
        adur = self.start_entry.get()
        bdur = self.end_entry.get()
        if adur != bdur:
            a = TIME_STR_CONVERTER(adur)
            b = TIME_STR_CONVERTER(bdur)
            if a < b:
                self.durTree.insert("", tk.END, values=(a,b))
                self.start_entry.delete(0, tk.END)
                self.end_entry.delete(0, tk.END)
            else:
                messagebox.showerror("bad entry", "start duration is greater then end")


    def extractClips(self):
        if self.titleEntry.get() == "":
            messagebox.showerror("bad entry", "title is required")
            return
        elif self.video_file == "" or self.music_file == "":
            messagebox.showerror("bad selection", "video or audio file is missing")
            return
        
        durs:list = []
        all_durs = self.durTree.get_children()
        for i in all_durs:
            durs.append(self.durTree.item(i)["values"])
        
        thread = threading.Thread(target=extract, args=(durs, self.video_file, self.music_file, self.titleEntry.get()))
        thread.start()


    def __init__(self, tab):
        self.root = tab
        self.setup_ui()
        

    def setup_ui(self):

        file_frame = tk.LabelFrame(self.root, text="Files")
        file_frame.pack(fill=tk.X, expand=True, padx=10, pady=4)

        def select_media(type):
            if type == "video":
                filetypes = (VIDEO_FILE_TUP, ALL_FILES_TUP)
                video = filedialog.askopenfilename(title="Select Video", filetypes=filetypes)
                if video:
                    self.video_file = video
                    video_file_btn["text"] = video
            elif type == "music":
                filetypes = (AUDIO_FILE_TUP, ALL_FILES_TUP)
                music = filedialog.askopenfilename(title="Select Music", filetypes=filetypes)
                if music:
                    self.music_file = music
                    music_file_btn["text"] = music

        video_file_btn = tk.Button(file_frame, text="Load Video File", width=50, command=lambda: select_media("video"))
        video_file_btn.grid(row=0, column=0, padx=10, pady=10)

        music_file_btn = tk.Button(file_frame, text="Load Music File", width=50, command=lambda: select_media("music"))
        music_file_btn.grid(row=0, column=1, padx=10, pady=10)

        input_frame = tk.LabelFrame(self.root, text="Duration Selection")
        input_frame.pack(fill=tk.X, expand=True, padx=10, pady=4)

        self.start_entry = tk.Entry(input_frame)
        self.start_entry.grid(row=0, column=0, padx=10, pady=10)

        self.end_entry = tk.Entry(input_frame)
        self.end_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(input_frame, text="Save", width=10, command=self.saveDur).grid(row=0, column=2, padx=10, pady=10)

        tk.Button(input_frame, text="Delete Selected", width=15, command=self.delete_one).grid(row=0, column=3, padx=10, pady=10)

        tk.Button(input_frame, text="Delete All", width=10, command=self.delete_all).grid(row=0, column=4, padx=10, pady=10)
        

        self.durTree = tk.ttk.Treeview(self.root, show="headings", selectmode="browse", columns=("start", "end"))
        self.durTree.pack(fill=tk.X, expand=True, padx=10, pady=4)

        self.durTree.column("start", width=80)
        self.durTree.column("end", width=80)
        self.durTree.heading("start", text="Start")
        self.durTree.heading("end", text="End")

        creation_frame = tk.LabelFrame(self.root, text="Creation")
        creation_frame.pack(fill=tk.X, expand=True, padx=10, pady=4)

        self.titleEntry = tk.Entry(creation_frame, width=100)
        self.titleEntry.grid(row=0, column=0, padx=10, pady=10)

        create_btn = tk.Button(creation_frame, text="Create", width=10, command=self.extractClips)
        create_btn.grid(row=0, column=1, padx=10, pady=10)

        self.root.mainloop()