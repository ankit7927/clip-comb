from src.audio import GenerateAudio
from src.video import GenerateClip, GenerateFinalCLip
from src.constants import IMAGE_WITH_ID, DELETE_ROW
import os, sqlite3

def create(data:list, backpath:str, vert:bool, conn:sqlite3.Connection, delete:bool, cate:str, removable:list):
    print(data)
    
    audiolist:list = GenerateAudio(data)

    cliplist:list = GenerateClip(data, backpath, vert, audiolist)

    GenerateFinalCLip(cliplist, data[0]["text"])

    for f in audiolist: os.remove(f)

    if delete:
        for i in removable:
            fname = conn.execute(IMAGE_WITH_ID(cate, i)).fetchone()
            os.remove(fname[0])
            conn.execute(DELETE_ROW(cate, i))
        print("removed old")