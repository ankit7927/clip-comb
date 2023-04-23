from .audio import GenerateAudio
from .video import GenerateClip, GenerateFinalCLip
from .gui import FactsData
import os

class ShortsMaker:
    data:dict = {}
    backPath:str = ""

    def __init__(self) -> None:
        self.data, self.backPath = FactsData().get()

        print(self.data)
        self.gen_audio()
        self.gen_clip()
        self.gen_final_clip()

    def gen_audio(self):
        GenerateAudio(self.data["title"]["text"], "title")
        
        for inx, i in enumerate(self.data["facts"]):
            GenerateAudio(i["fact"], inx)
    
    def gen_clip(self):
        GenerateClip(True, self.data["title"]["image"], None, None)

        for inx, i in enumerate(self.data["facts"]):
            GenerateClip(False, i["image"], inx, inx)

    def gen_final_clip(self):
        GenerateFinalCLip(len(self.data["facts"]), self.backPath, self.data["title"]["text"])
        print("cleaning raw")
        for f in os.listdir("src/raw"): os.remove("src/raw/"+f)