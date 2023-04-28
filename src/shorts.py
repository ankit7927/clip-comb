from .audio import GenerateAudio
from .video import GenerateClip, GenerateFinalCLip
from .gui import FactsData
import os

class ShortsMaker:
    data:dict = []
    backPath:str = ""

    def __init__(self) -> None:
        #self.data, self.backPath = FactsData().get()
        self.data = [{"text":"this is an best facts", "image":"image.jpeg"}]
        self.backPath = "backs.mp4"

        print(self.data)
        self.gen_audio()
        GenerateClip(self.data, self.backPath)
        self.gen_final_clip()

    def gen_audio(self):
        for inx, i in enumerate(self.data):
            GenerateAudio(i["text"], inx)
    

    def gen_final_clip(self):
        GenerateFinalCLip(len(self.data), self.data[0]["text"])
        print("cleaning raw")
        for f in os.listdir("src/raw"): os.remove("src/raw/"+f)