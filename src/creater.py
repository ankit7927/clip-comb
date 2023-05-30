from src.audio import GenerateAudio
from src.video import GenerateClip, ExtractClip
from src.constants import IMAGE_WITH_ID, DELETE_ROW
import os, sqlite3

def create(data:list, backpath:str, vert:bool, conn:sqlite3.Connection, delete:bool, cate:str, removable:list):
    print(data)
    
    audiolist:list = GenerateAudio(data)

    GenerateClip(data, backpath, vert, audiolist, data[0]["text"])

    for f in audiolist: os.remove(f)

    if delete:
        for i in removable:
            fname = conn.execute(IMAGE_WITH_ID(cate, i)).fetchone()
            os.remove(fname[0])
            conn.execute(DELETE_ROW(cate, i))
        print("removed old")

def extract(durs:list, videofile:str, audiofile:str, fname:str):
    ExtractClip(durations=durs, videopath=videofile, audiopath=audiofile, fname=fname)
    
