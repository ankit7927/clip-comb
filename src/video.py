import moviepy.editor as mp
from moviepy.video.fx.crop import crop
from moviepy.video.fx.all import speedx
from moviepy.audio.fx.volumex import volumex
from src.constants import *

FONT_PATH = "RobotoSlab-Medium.ttf"

def Back16x9(backPath:str) -> mp.VideoClip:
    """Crop Horizontal Background Clip"""
    back:mp.VideoClip = mp.VideoFileClip(backPath)

    width = back.size[0]
    height = int(width * 9 / 16)
    y_offset = int((back.size[1] - height) / 2)

    return crop(back, x1=0, y1=y_offset, x2=width, y2=y_offset + height)

def Back9x16(backPath:str) -> mp.VideoClip:
    """Crop Vertical Background Clip"""
    back:mp.VideoClip = mp.VideoFileClip(backPath)

    height = back.size[1]
    width = int(height * 9 / 16)
    x_offset = int((back.size[0] - width) / 2)

    return crop(back, x1=x_offset, y1=0, x2=x_offset + width, y2=height)

def GenerateClip(data:list, backpath:str, vert:bool, audiolist:list) -> list:
    IMAGE_POS = VER_IMAGE_POS if vert else HOR_IMAGE_POS
    IMAGE_HEIGHT = VER_IMAGE_HEIGHT if vert else HOR_IMAGE_HEIGHT
    TEXT_POS = VER_TEXT_POS if vert else HOR_TEXT_POS
    TEXT_SIZE = VER_TEXT_SIZE if vert else HOR_TEXT_SIZE

    if vert: back_clip:mp.VideoClip = Back9x16(backPath=backpath)
    else : back_clip:mp.VideoClip = Back16x9(backPath=backpath)
    
    cliplist:list = []
    last_dur = 0
    for inx in range(len(data)):
        try:
            fname = CLIP_NAME(RANDOM_NAME())
            audio_clip = mp.AudioFileClip(audiolist[inx])

            img_clip = mp.ImageClip(data[inx]["image"]).set_position(IMAGE_POS)
            img_clip = img_clip.resize(height=IMAGE_HEIGHT)
            img_clip.duration = audio_clip.duration
            img_clip = img_clip.set_audio(audio_clip)
            img_clip = img_clip.fx(speedx, AUDIO_SPEED)
            img_clip = img_clip.fx(volumex, AUDIO_VOLUME)

            text_clip = mp.TextClip(data[inx]["text"], font=FONT_NAME, fontsize=35, color='white', bg_color='transparent', align='center', method='caption', size=TEXT_SIZE)
            text_clip = text_clip.set_position(TEXT_POS, relative=True)

            back_clip = back_clip.subclip(last_dur)
 
            con_clip = mp.CompositeVideoClip([back_clip, img_clip, text_clip], use_bgclip=True)
            con_clip.duration = img_clip.duration
            con_clip.write_videofile(fname)
            cliplist.append(fname)
            last_dur += img_clip.duration

        except Exception as e:
            print(e)
    return cliplist

def GenerateFinalCLip(cliplist:list, fname:str):
    clip_chunks:list = []
    for clip in cliplist:
        clip_chunks.append(mp.VideoFileClip(clip))

    final_clip =  mp.concatenate_videoclips(clip_chunks, method="compose")
    
    final_clip.write_videofile(FINAL_CLIP_NAME(fname[:99]), codec='libx264', audio_codec='aac')