from gtts import gTTS

def GenerateAudio(text:str, fname:str):
    language = 'en'
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save(f"src/raw/{fname}.mp3")

#GenerateAudio("hello world, how are you", "test")