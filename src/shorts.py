from .audio import GenerateAudio
from .video import GenerateClip, GenerateFinalCLip
from .gui import DataCollector
import os

class ShortsMaker:
    data:dict = []
    backPath:str = ""

    def __init__(self) -> None:
        self.data, self.backPath = DataCollector().get()

        print(self.data)
        self.gen_audio()
        GenerateClip(self.data, self.backPath)
        self.gen_final_clip()

    def gen_audio(self):
        for inx, i in enumerate(self.data):
            GenerateAudio(i["text"], inx)
    
    def gen_final_clip(self):
        GenerateFinalCLip(len(self.data), self.data[0]["text"])
        print("cleaning temp")
        for f in os.listdir("src/temp"): os.remove("src/temp/"+f)