import moviepy.editor as mp
from moviepy.video.fx.crop import crop

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
