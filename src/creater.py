from src.audio import GenerateAudio
from src.video import GenerateClip, ExtractClip
from src.utility import DownloadImage
import os

def create(data:list, backpath:str, temp:str):
    print(data)
    
    print("getting audio")
    audiolist:list = GenerateAudio(data)

    print("getting images")
    imagelist = DownloadImage(data)

    GenerateClip(data, backpath, temp, audiolist, imagelist, data[0]["text"])

    for f in audiolist: os.remove(f)
    for f in imagelist: os.remove(f)

def extract(durs:list, videofile:str, audiofile:str, fname:str):
    ExtractClip(durations=durs, videopath=videofile, audiopath=audiofile, fname=fname)
    
