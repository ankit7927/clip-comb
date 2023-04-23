import moviepy.editor as mp
from moviepy.video.fx.crop import crop
from moviepy.video.fx.all import speedx, resize
from moviepy.audio.fx.volumex import volumex


def Background(backPath:str) -> mp.VideoClip:
    back:mp.VideoClip = mp.VideoFileClip(backPath)
    
    (w, h) = back.size
    crpwidth = h * 9/16

    x1, x2 = (w-crpwidth)//2, (w+crpwidth)//2
    y1, y2 = 0, h

    return crop(back, x1=x1, x2=x2, y1=y1, y2=y2)

def GenerateClip(title:bool, imgPath:str, audio:str, output:str):
    if title:
        audio_clip = mp.AudioFileClip("src/raw/title.mp3")
        img_clip = mp.ImageClip(imgPath)

        img_clip = img_clip.set_audio(audio_clip)
        img_clip.duration = audio_clip.duration
        img_clip = img_clip.fx(speedx, 1.2)
        img_clip = img_clip.fx(resize, 0.4)
        img_clip.fps = 1
        img_clip.write_videofile("src/raw/title.mp4")

    else:
        audio_clip = mp.AudioFileClip(f"src/raw/{audio}.mp3")
        img_clip = mp.ImageClip(imgPath)

        img_clip = img_clip.set_audio(audio_clip)
        img_clip.duration = audio_clip.duration
        img_clip = img_clip.fx(speedx, 1.2)
        img_clip = img_clip.fx(resize, 0.4)
        img_clip.fps = 1
        img_clip.write_videofile(f"src/raw/{output}.mp4")

def addChunks(lenth:int):
    list_chunks:list = [mp.VideoFileClip("src/raw/title.mp4")]
    for i in range(0, lenth):
        list_chunks.append(mp.VideoFileClip(f"src/raw/{str(i)}.mp4"))
    return mp.concatenate_videoclips(list_chunks, method="compose").set_position(lambda t: ('center', 50+t))
    

def GenerateFinalCLip(lenth:int, backPath:str, fname:str):
    background:mp.VideoClip = Background(backPath)
    ovelay:mp.VideoClip = addChunks(lenth)
    ovelay = ovelay.fx(volumex, 2.0)

    if ovelay.duration > background.duration:
        background = mp.concatenate_videoclips([background, background])
    
    background = background.subclip(0, ovelay.duration)

    final_clip = mp.CompositeVideoClip(clips=[background, ovelay], use_bgclip=True)
    final_clip.write_videofile(f"{fname}.mp4")










