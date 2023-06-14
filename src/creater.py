from src.audio import GenerateAudio
from src.video import GenerateClip, ExtractClip
import os

def create(data:list, backpath:str, temp:str):
    print(data)
    
    audiolist:list = GenerateAudio(data)

    GenerateClip(data, backpath, temp, audiolist, data[0]["text"])

    for f in audiolist: os.remove(f)

def extract(durs:list, videofile:str, audiofile:str, fname:str):
    ExtractClip(durations=durs, videopath=videofile, audiopath=audiofile, fname=fname)
    
