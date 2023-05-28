import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from tkVideoPlayer import TkinterVideo
from src.creater import extract
import threading

class Extractor:

    varA = 0
    varB = 0

    def update_duration(self, event):
        duration = self.vid_player.video_info()["duration"]
        self.end_time["text"] = str(datetime.timedelta(seconds=duration))
        self.progress_slider["to"] = duration


    def update_scale(self, event):
        current_time = self.vid_player.current_duration()
        minutes = current_time // 60
        seconds = current_time % 60
        self.progress_value.set(current_time)
        self.start_time["text"] = str(datetime.timedelta(minutes=minutes, seconds=seconds))



    def load_video(self):
        self.file_path = filedialog.askopenfilename()

        if self.file_path:
            self.vid_player.load(self.file_path)

            self.progress_slider.config(to=0, from_=0)
            self.play_pause_btn["text"] = "Play"
            self.progress_value.set(0)
            self.vid_player.play()


    def seek(self, value):
        """ used to seek a specific timeframe """
        self.vid_player.seek(int(value))


    def play_pause(self):
        if self.file_path != "":
            if self.vid_player.is_paused():
                self.vid_player.play()
            else:
                self.vid_player.pause()


    def video_ended(self, event):
        duration = self.vid_player.video_info()["duration"]
        minutes = duration // 60
        seconds = duration % 60
        self.progress_slider.set(self.progress_slider["to"])
        self.play_pause_btn["text"] = "Play"
        self.start_time["text"] = str(datetime.timedelta(minutes=minutes, seconds=seconds))
        self.progress_slider.set(0)
        self.progress_value.set(0)

    def setA(self):
        self.varA = self.progress_value.get()
        self.btnA["text"] = self.varA
        if not self.vid_player.is_paused():
            self.vid_player.pause()

    def setB(self):
        self.varB = self.progress_value.get()
        self.btnB["text"] = self.varB
        if not self.vid_player.is_paused():
            self.vid_player.pause()

    def saveAB(self):
        if self.varA != self.varB and self.varA < self.varB:
            self.durTree.insert("", tk.END, values=(self.varA, self.varB))
            self.varA = 0
            self.varB = 0
            self.btnA["text"] = "A"
            self.btnB["text"] = "B"


    def extractClips(self):
        if self.titleEntry.get() == "":
            messagebox.showerror("bad entry", "title is required")
            return
        durs:list = []
        all_durs = self.durTree.get_children()
        for i in all_durs:
            durs.append(self.durTree.item(i)["values"])
        
        thread = threading.Thread(target=extract, args=(durs, self.file_path, self.titleEntry.get()))
        thread.start()


    def __init__(self, tab):
        self.root = tab
        self.setup_ui()
        

    def setup_ui(self):
        
        videoframe = tk.LabelFrame(self.root, text="video player")
        videoframe.pack(fill=tk.BOTH, padx=5, pady=10, side=tk.LEFT)

        self.vid_player = TkinterVideo(scaled=True, master=videoframe)
        self.vid_player.pack(expand=True, fill="both")

        playcont = tk.LabelFrame(videoframe, text="Play Controll")
        playcont.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=10)

        load_btn = tk.Button(playcont, text="Load", command=self.load_video, width=10)
        load_btn.grid(row=0, column=0, padx=5, pady=10, sticky=tk.NW)

        self.play_pause_btn = tk.Button(playcont, text="Pause/Play", command=self.play_pause, width=10)
        self.play_pause_btn.grid(row=0, column=1, padx=5, pady=10, sticky=tk.NW)

        self.start_time = tk.Label(playcont, text=str(datetime.timedelta(seconds=0)))
        self.start_time.grid(row=0, column=2, padx=10, pady=10, sticky=tk.NW)

        self.end_time = tk.Label(playcont, text=str(datetime.timedelta(seconds=0)))
        self.end_time.grid(row=0, column=3, padx=10, pady=10, sticky=tk.NW)

        self.btnA = tk.Button(playcont, text="A", width=10, command=self.setA, anchor=tk.NW)
        self.btnA.grid(row=0, column=4)

        self.btnB = tk.Button(playcont, text="B", width=10, command=self.setB, anchor=tk.NW)
        self.btnB.grid(row=0, column=5, padx=5, pady=10)

        self.progress_value = tk.DoubleVar(playcont)

        self.progress_slider = tk.Scale(playcont, variable=self.progress_value, from_=0, to=0, orient="horizontal", command=self.seek, length=400)
        self.progress_slider.grid(row=1, columnspan=4, padx=5, pady=10)

        self.btnSave = tk.Button(playcont, text="Save", width=20, command=self.saveAB)
        self.btnSave.grid(row=1, column=4, columnspan=2)

        self.vid_player.bind("<<Duration>>", self.update_duration)
        self.vid_player.bind("<<SecondChanged>>", self.update_scale)
        self.vid_player.bind("<<Ended>>", self.video_ended )

        controlframe = tk.LabelFrame(self.root, text="video player")
        controlframe.pack(fill=tk.BOTH, expand=True, pady=10, side=tk.RIGHT)

        delete_btn = tk.Button(controlframe, text="Delete")
        delete_btn.pack(fill=tk.X, padx=5)

        self.durTree = tk.ttk.Treeview(controlframe, show="headings", selectmode="browse", columns=("start", "end"))
        self.durTree.pack(padx=5, pady=10)

        self.durTree.column("start", width=80)
        self.durTree.column("end", width=80)
        self.durTree.heading("start", text="Start")
        self.durTree.heading("end", text="End")

        self.titleEntry = tk.Entry(controlframe)
        self.titleEntry.pack(fill=tk.X, padx=5)
    
        tk.Button(controlframe, text="Create", command=self.extractClips).pack(fill=tk.X, padx=5, pady=10)


        self.root.mainloop()