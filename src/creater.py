from src.audio import GenerateAudio
from src.video import GenerateClip, GenerateFinalCLip
from src.constants import TEMP_DIR
import os 

def create(data, backpath, vert, delete):
    print(data)
    
    audiolist:list = GenerateAudio(data)

    cliplist:list = GenerateClip(data, backpath, vert, audiolist)

    GenerateFinalCLip(cliplist, data[0]["text"])

    for f in cliplist: os.remove(f)
    for f in audiolist: os.remove(f)