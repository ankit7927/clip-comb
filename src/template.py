import moviepy.editor as mp
from moviepy.video.fx.all import speedx
from moviepy.audio.fx.volumex import volumex
from src.constants import *
from src.utility import *

def tempV1_VERTICAL(data:list, backpath:str, audiolist:list, fname):
    back_clip:mp.VideoClip = Crop9x16(backPath=backpath, clip=None)
    list_imgs = downloadImage(data)

    cliplist:list = []
    last_dur:int = 0
    
    for inx in range(len(data)):
        try:
            audio_clip = mp.AudioFileClip(audiolist[inx])

            img_clip = mp.ImageClip(list_imgs[inx]).set_position(VER_IMAGE_POS)
            img_clip = img_clip.resize(height=VER_IMAGE_HEIGHT)
            img_clip.duration = audio_clip.duration
            img_clip = img_clip.set_audio(audio_clip)
            img_clip = img_clip.fx(speedx, AUDIO_SPEED)
            img_clip = img_clip.fx(volumex, AUDIO_VOLUME)


            text_clip_duration = img_clip.duration / len(data[inx]["text"].split())
            text_clips = []
            for text in data[inx]["text"].split():
                text_clip = mp.TextClip(text, fontsize=70, font=FONT_ROBOTO, color='white', stroke_color="black", stroke_width=3, bg_color='transparent', method='label')
                text_clip.duration = text_clip_duration
                text_clip.fps = 1
                text_clips.append(text_clip)
            text_clip = mp.concatenate_videoclips(text_clips)
            

            text_clip = text_clip.set_position(VER_TEXT_POS, relative=True)
 
            back_clip = back_clip.subclip(last_dur)
 
            com_clip = mp.CompositeVideoClip([back_clip, img_clip, text_clip], use_bgclip=True)
            com_clip.duration = img_clip.duration
            cliplist.append(com_clip)
            last_dur += img_clip.duration

        except Exception as e:
            print(e)
    
    final_clip:mp.CompositeVideoClip = mp.concatenate_videoclips(cliplist, method="compose")
    final_clip.write_videofile(FINAL_CLIP_NAME(fname[:99]))

    back_clip.close()

def tempV1_HORIZONTAL(data:list, backpath:str, audiolist:list, fname):
    back_clip:mp.VideoClip = Crop16x9(backPath=backpath, clip=None)
    list_imgs = downloadImage(data)
    
    cliplist:list = []
    last_dur:int = 0
    
    
    for inx in range(len(data)):
        try:
            audio_clip = mp.AudioFileClip(audiolist[inx])

            img_clip = mp.ImageClip(list_imgs[inx]).set_position(HOR_IMAGE_POS)
            img_clip = img_clip.resize(height=HOR_IMAGE_HEIGHT)
            img_clip.duration = audio_clip.duration
            img_clip = img_clip.set_audio(audio_clip)
            img_clip = img_clip.fx(speedx, AUDIO_SPEED)
            img_clip = img_clip.fx(volumex, AUDIO_VOLUME)

            text_clip = mp.TextClip(data[inx]["text"], font=FONT_ROBOTO, fontsize=35, color='white', bg_color='transparent', align='center', method='caption', size=HOR_TEXT_SIZE)

            text_clip = text_clip.set_position(HOR_TEXT_POS, relative=True)
 
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

def tempV3(data:list, audiolist:list, fname):
    list_imgs = downloadImage(data)
    cliplist:list = []

    for inx in range(len(data)):
        audio_clip = mp.AudioFileClip(audiolist[inx])

        main_image = CropInSquare(None, mp.ImageClip(list_imgs[inx]))
        main_image.duration = audio_clip.duration
        main_image = main_image.set_audio(audio_clip)
        main_image = main_image.fx(speedx, AUDIO_SPEED)
        main_image = main_image.fx(volumex, AUDIO_VOLUME)
        main_image.fps = 1

        cliplist.append(main_image)

    title_image = mp.ImageClip("src/assets/title1.jpg")

    main_image_clip = mp.concatenate_videoclips(cliplist, method="compose")

    title_image = title_image.resize(width=main_image_clip.size[0])
    
    main_image_clip = main_image_clip.set_position((0, title_image.size[1]))

    final_clip:mp.CompositeVideoClip = mp.CompositeVideoClip([title_image, main_image_clip], size=(title_image.w, title_image.h+main_image_clip.h))
    final_clip.duration = main_image_clip.duration
    final_clip.write_videofile(FINAL_CLIP_NAME(fname[:99]))