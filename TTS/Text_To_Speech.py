from gtts import gTTS
import os

def test(usrText):
    #test = 'Test Audio'
    language = 'en'

    player = gTTS(text=usrText, lang = language, slow=False)
    print("Saving TTS")
    player.save("C:\Projects\Personal\AleBot2.0\TTS/audio_cache/temp.mp3")
    #os.system("temp.mp3")

def test_lang(usrText, lang):
    language = lang
    
    player = gTTS(text=usrText, lang = language, slow=False)
    print("Saving TTS w/ custom language")
    player.save("C:\Projects\Personal\AleBot2.0\TTS/audio_cache/temp.mp3")