from gtts import gTTS
from src.constants import AUDIO_NAME, RANDOM_NAME

def GenerateAudio(data:list):
    language = 'en'
    audiolits:list = []
    for text in data:
        fname = AUDIO_NAME(RANDOM_NAME())
        myobj = gTTS(text=text["text"], lang=language, slow=False)
        myobj.save(fname)
        audiolits.append(fname)
    return audiolits