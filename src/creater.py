from src.audio import GenerateAudio
from src.video import GenerateClip, ExtractClip
from src.utility import DownloadImage

def create(data:list, backpath:str, temp:str):
    print(data)

    new_data, imagelist = DownloadImage(data)

    audiolist:list = GenerateAudio(new_data)

    GenerateClip(new_data, backpath, temp, audiolist, imagelist, new_data[0]["text"])

def extract(durs:list, videofile:str, audiofile:str, fname:str):
    ExtractClip(durations=durs, videopath=videofile, audiopath=audiofile, fname=fname)
    
