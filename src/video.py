import moviepy.editor as mp
import moviepy.video.fx.all as vfx
from src.utility import *
from src.constants import *
from src.template import *


def GenerateClip(data:list, backpath:str, temp:str, audiolist:list, imagelist, fname) -> list:
    if temp == "vertical":
        tempV1_VERTICAL(data=data, backpath=backpath, audiolist=audiolist, imagelist=imagelist, fname=fname)
    elif temp == "horizontal":
        tempV1_HORIZONTAL(data=data, backpath=backpath, audiolist=audiolist, fname=fname)
    else:
        print("unknown template selected")
        return

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

    final_clip:mp.CompositeVideoClip = mp.concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(FINAL_CLIP_NAME(fname[:99]))

    video.close()
    audio.close()
