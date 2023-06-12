from src.audio import GenerateAudio
from src.video import ExtractClip
from src.template import *
import os

def create(data:list):
    print(data)
    
    audiolist:list = GenerateAudio(data)

    tempV3(data=data, audiolist=audiolist, fname=data[0]["text"])

def extract(durs:list, videofile:str, audiofile:str, fname:str):
    ExtractClip(durations=durs, videopath=videofile, audiopath=audiofile, fname=fname)
    
