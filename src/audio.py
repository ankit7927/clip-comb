from gtts import gTTS
from src.constants import AUDIO_NAME

def GenerateAudio(text:str, fname:str):
    language = 'en'
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save(AUDIO_NAME(fname))