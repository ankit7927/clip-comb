import moviepy.editor as mp
from moviepy.video.fx.crop import crop
from moviepy.video.fx.all import speedx
from moviepy.audio.fx.volumex import volumex
import moviepy.video.fx.all as vfx
from src.constants import *

FONT_PATH = "RobotoSlab-Medium.ttf"

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

def GenerateClip(data:list, backpath:str, vert:bool, audiolist:list, fname) -> list:
    IMAGE_POS = VER_IMAGE_POS if vert else HOR_IMAGE_POS
    IMAGE_HEIGHT = VER_IMAGE_HEIGHT if vert else HOR_IMAGE_HEIGHT
    TEXT_POS = VER_TEXT_POS if vert else HOR_TEXT_POS
    TEXT_SIZE = VER_TEXT_SIZE if vert else HOR_TEXT_SIZE

    if vert: back_clip:mp.VideoClip = Crop9x16(backPath=backpath, clip=None)
    else : back_clip:mp.VideoClip = Crop16x9(backPath=backpath, clip=None)
    
    cliplist:list = []
    last_dur:int = 0
    for inx in range(len(data)):
        try:
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
            cliplist.append(con_clip)
            last_dur += img_clip.duration
        except Exception as e:
            print(e)
    
    final_clip:mp.CompositeVideoClip = mp.concatenate_videoclips(cliplist, method="compose")
    final_clip.write_videofile(FINAL_CLIP_NAME(fname[:99]))

    back_clip.close()


def ExtractClip(durations:list, videopath:str, audiopath:str, fname:str):
    video:mp.VideoClip = mp.VideoFileClip(videopath)
    audio:mp.AudioClip = mp.AudioFileClip(audiopath)

    clips:list = []

    for duration in durations:
        try:
            clip:mp.VideoClip = video.subclip(duration[0], duration[1])
            clip = Crop9x16(backPath=None, clip=clip)
            clip = clip.fx(vfx.lum_contrast, lum=0.5, contrast=0.5, contrast_thr=100)
            clip = clip.crossfadein(1.4)
            clips.append(clip)
        except Exception as e:
            print(e)

    final_clip:mp.CompositeVideoClip = mp.concatenate_videoclips(clips, method="chain")
    final_clip.write_videofile(FINAL_CLIP_NAME(fname[:99]))

    video.close()
    audio.close()