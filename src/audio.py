from gtts import gTTS

def GenerateAudio(text:str, fname:str):
    language = 'en'
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save(f"src/temp/{fname}.mp3")