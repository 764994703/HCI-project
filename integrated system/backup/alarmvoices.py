import pyttsx3
import win32com
import pygame
import time

def readscore(score):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for item in voices:
        print(item.id, item.languages)
    engine.setProperty("voice","HKEY_LOCAL_MACHINE/SOFTWARE/Microsoft/Speech/Voices/Tokens/TTS_MS_ZH-CN_HUIHUI_11.0")
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-15)
    engine.say(str(score) + "分")
    engine.runAndWait()



def emergency():
    file = "C:/Users/hasee/Desktop/skin-python/voices/sleepy.mp3"
    
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

def angry():
    file = "C:/Users/hasee/Desktop/skin-python/voices/angry1.mp3"
    
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

def score(score):
    file1 = "C:/Users/hasee/Desktop/skin-python/voices/score1.mp3"
    if(score > 80):
        file2 = "C:/Users/hasee/Desktop/skin-python/voices/score-lowrisk.mp3"
    else:
        file2 = "C:/Users/hasee/Desktop/skin-python/voices/score-highrisk.mp3"
    
    
    
    pygame.mixer.music.load(file1)
    pygame.mixer.music.play()
    time.sleep(3)
    pygame.mixer.music.stop()
    readscore(score)
    
    pygame.mixer.music.load(file2)
    pygame.mixer.music.play()

if __name__ == '__main__':
    pygame.mixer.init()
    score(88)
    
