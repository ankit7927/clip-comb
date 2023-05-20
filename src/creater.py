from src.audio import GenerateAudio
from src.video import GenerateClip, GenerateFinalCLip
from src.constants import TEMP_DIR
import os 

def create(data, backpath, vert, delete):
    print(data)
    
    for inx, i in enumerate(data):
        print(f"Fetching Audio {inx}")
        GenerateAudio(i["text"], inx)

    print("generating clips")
    GenerateClip(data, backpath, vert)

    print("generating final clip")
    GenerateFinalCLip(len(data), data[0]["text"])

    if delete:
        print("cleaning temp")
        for f in os.listdir(TEMP_DIR): os.remove(TEMP_DIR+f)