from .audio import GenerateAudio
from .video import GenerateClip, GenerateFinalCLip
from .gui.collector import Collector
import os, sys
from src.constants import TEMP_DIR

class ShortsMaker:
    data:dict = []

    def __init__(self) -> None:
        collector = Collector()
        self.data, backPath, font = collector.get()

        if len(self.data) == 0: sys.exit(0)

        print(self.data)

        self.gen_audio()
        GenerateClip(self.data, backPath, font)
        self.gen_final_clip()
        collector.removeOld()

    def gen_audio(self):
        for inx, i in enumerate(self.data):
            GenerateAudio(i["text"], inx)
    
    def gen_final_clip(self):
        GenerateFinalCLip(len(self.data), self.data[0]["text"])
        print("cleaning temp")
        for f in os.listdir(TEMP_DIR): os.remove(TEMP_DIR+f)