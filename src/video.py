import moviepy.editor as mp
from moviepy.video.fx.crop import crop
from moviepy.video.fx.all import speedx
from moviepy.audio.fx.volumex import volumex


font_path = "src/fonts/"

def Background(backPath:str) -> mp.VideoClip:
    back:mp.VideoClip = mp.VideoFileClip(backPath)
    
    (w, h) = back.size
    crpwidth = h * 9/16

    x1, x2 = (w-crpwidth)//2, (w+crpwidth)//2
    y1, y2 = 0, h

    return crop(back, x1=x1, x2=x2, y1=y1, y2=y2)

def GenerateClip(data:list, backpath:str, font:str):
    last_dur = 0
    for inx, i in enumerate(data):
        audio_clip = mp.AudioFileClip(f"src/temp/{inx}.mp3")
        img_clip = mp.ImageClip(data[inx]["image"]).set_position(lambda t: ('center', 50+t))
        img_clip = img_clip.resize(height=300)
        img_clip.duration = audio_clip.duration
        img_clip = img_clip.set_audio(audio_clip)
        img_clip = img_clip.fx(speedx, 1.2)
        img_clip = img_clip.fx(volumex, 2)

        text_clip = mp.TextClip(data[inx]["text"], font=font_path+font, fontsize=35, color='white', bg_color='transparent', align='center', method='caption', size=(480, None))
        text_clip = text_clip.set_position(("center",0.7), relative=True)
        
        back_clip:mp.VideoClip = Background(backPath=backpath)
        back_clip = back_clip.subclip(last_dur, img_clip.duration)
        
        con_clip = mp.CompositeVideoClip([back_clip, img_clip, text_clip], use_bgclip=True)
        con_clip.duration = img_clip.duration
        con_clip.write_videofile(f"src/temp/{inx}_clp.mp4")
        last_dur += img_clip.duration


def GenerateFinalCLip(lenth:int, fname:str):
    clip_chunks:list = []
    for i in range(0, lenth):
        clip_chunks.append(mp.VideoFileClip(f"src/temp/{str(i)}_clp.mp4"))
    final_clip =  mp.concatenate_videoclips(clip_chunks, method="compose")
    
    final_clip.write_videofile(f"{fname}.mp4", codec='libx264', audio_codec='aac')
