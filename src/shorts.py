from .audio import GenerateAudio
from .video import GenerateClip, GenerateFinalCLip
from src.gui.manager import Manager
import os
from src.constants import TEMP_DIR

class ShortsMaker:
    data:dict = []

    def __init__(self) -> None:
        manager = Manager()
        self.data, backPath, font = manager.get()
        
        print(self.data)

        self.gen_audio()
        GenerateClip(self.data, backPath, font)
        self.gen_final_clip()
        manager.removeOld()

    def gen_audio(self):
        for inx, i in enumerate(self.data):
            print(f"Fetching Audio {inx}")
            GenerateAudio(i["text"], inx)
    
    def gen_final_clip(self):
        GenerateFinalCLip(len(self.data), self.data[0]["text"])
        print("cleaning temp")
        for f in os.listdir(TEMP_DIR): os.remove(TEMP_DIR+f)