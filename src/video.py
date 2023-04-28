import moviepy.editor as mp
from moviepy.video.fx.crop import crop
from moviepy.video.fx.all import speedx, resize
from moviepy.audio.fx.volumex import volumex


max_width = 1080
max_height = 1920
font_path = "Poppins-Regular.ttf"

def text_wrap(text, width):
    words = text.split()
    lines = []
    current_line = words[0]
    for word in words[1:]:
        if len(current_line + ' ' + word) <= width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines

def Background(backPath:str) -> mp.VideoClip:
    back:mp.VideoClip = mp.VideoFileClip(backPath)
    
    (w, h) = back.size
    crpwidth = h * 9/16

    x1, x2 = (w-crpwidth)//2, (w+crpwidth)//2
    y1, y2 = 0, h

    return crop(back, x1=x1, x2=x2, y1=y1, y2=y2)

def GenerateClip(facts:list, backpath:str):
    last_dur = 0
    for inx, i in enumerate(facts):
        audio_clip = mp.AudioFileClip(f"src/raw/{inx}.mp3")
        img_clip = mp.ImageClip(facts[inx]["image"]).set_position(lambda t: ('center', 50+t))
        img_clip = img_clip.resize(height=300)
        img_clip.duration = audio_clip.duration
        img_clip = img_clip.set_audio(audio_clip)
        img_clip = img_clip.fx(speedx, 1.2)


        text_clip = mp.TextClip(facts[inx]["text"], font=font_path, fontsize=30, color='white', bg_color='transparent', align='center', method='caption', size=(max_width, None))
        text_clip = text_clip.set_position(('center','bottom'))

        if text_clip.w > max_width:
            wrapped_lines = []
            for line in facts[inx]["text"]:
                wrapped_lines.extend(text_wrap(line, max_width))
            text_clip = mp.TextClip('\n'.join(wrapped_lines), font=font_path, fontsize=30, color='white', bg_color='transparent', align='center', method='caption', size=(max_width, None))
            text_clip = text_clip.set_position(('center','bottom'))

        back_clip:mp.VideoClip = Background(backPath=backpath)
        back_clip = back_clip.subclip(last_dur, img_clip.duration)
        
        con_clip = mp.CompositeVideoClip([back_clip, img_clip, text_clip], use_bgclip=True)
        con_clip.duration = img_clip.duration
        con_clip.write_videofile(f"src/raw/{inx}_clp.mp4")
        last_dur += img_clip.duration

def GenerateFinalCLip(lenth:int, fname:str):

    clip_chunks:list = []
    for i in range(0, lenth):
        clip_chunks.append(mp.VideoFileClip(f"src/raw/{str(i)}_clp.mp4"))
    final_clip =  mp.concatenate_videoclips(clip_chunks, method="compose")
    
    final_clip.write_videofile(f"{fname}.mp4", codec='libx264', audio_codec='aac')
    
