import pyttsx3
import pygame
import random
import time
import os
import win32com


class PlayMp3:
    def __init__(self):
        pygame.mixer.init()
        pygame.init()
        
    def play(self, path):
        if(pygame.mixer.music.get_busy()):
            return
        nextSound = pygame.mixer.Sound(path)
        pygame.mixer.Channel(0).queue(nextSound)
        # print(pygame.mixer.Channel(0).get_queue())
        return
    
    def emergentplay(self, path):
        if(pygame.mixer.music.get_busy()):
            return
        pygame.mixer.Channel(0).stop()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()


def test():
    x = PlayMp3()
    x.noeyes()
    x.noface()
    x.tired()


if __name__ == "__main__":
    test()
