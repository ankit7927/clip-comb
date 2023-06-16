import moviepy.editor as mp
from moviepy.video.fx.crop import crop
import requests
from src.constants import TEMP_DIR, RANDOM_NAME


def DownloadImage(data:list) -> list:
    list_imgs:list = []
    new_data:list = []
    for inx, d in enumerate(data):
        print(f"Downloading image {inx+1}")
        try:
            temp_img = TEMP_DIR +RANDOM_NAME()+"."+d["image"].split(".")[-1]
            with open(temp_img, "wb") as f:
                f.write(requests.get(d["image"]).content)
            list_imgs.append(temp_img)
            new_data.append(d)
        except Exception as e:
            print(e)
    return new_data, list_imgs

def Crop16x9(backPath:str, clip:mp.VideoClip) -> mp.VideoClip:
    """Crop Horizontal Background Clip"""
    back:mp.VideoClip = None 

    if backPath and not clip:
        back = mp.VideoFileClip(backPath)
    elif clip and not backPath:
        back = clip

    width = back.size[0]
    height = int(width * 9 / 16)
    y_offset = int((back.size[1] - height) / 2)

    return crop(back, x1=0, y1=y_offset, x2=width, y2=y_offset + height)

def Crop9x16(backPath:str, clip:mp.VideoClip) -> mp.VideoClip:
    """Crop Vertical Background Clip"""
    back:mp.VideoClip = None 

    if backPath and not clip:
        back = mp.VideoFileClip(backPath)
    elif clip and not backPath:
        back = clip

    height = back.size[1]
    width = int(height * 9 / 16)
    x_offset = int((back.size[0] - width) / 2)

    return crop(back, x1=x_offset, y1=0, x2=x_offset + width, y2=height)
