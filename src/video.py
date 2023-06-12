import moviepy.editor as mp
import moviepy.video.fx.all as vfx
from src.utility import *
from src.constants import *


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