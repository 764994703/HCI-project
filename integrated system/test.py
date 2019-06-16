import pygame
import time
import cv2
import threading
import math
import GUI
import wx

voice1 = "./voices/noEyes.mp3"
voice2 = "./voices/noFace.mp3"


def pygame_test1():
    pygame.mixer.init()
    pygame.mixer.music.load(voice1)
    pygame.mixer.music.play()
    time.sleep(1)
    pygame.mixer.music.load(voice2)
    pygame.mixer.music.play()
    while True:
        time.sleep(10)


def pygame_test2():
    pygame.mixer.init()
    track2 = pygame.mixer.Sound(voice1)
    track2.play()


def pygame_test3():
    pygame.mixer.init()
    # pygame.mixer.music.load(voice1)
    # pygame.mixer.music.play()
    # time.sleep(1)
    pygame.mixer.music.queue(voice2)

    while True:
        time.sleep(10)


class TestCV2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        video_capture = cv2.VideoCapture(0)  # 0为默认摄像头
        VIDEO_FPS = math.ceil(video_capture.get(cv2.CAP_PROP_FPS))
        print("FPS: " + str(VIDEO_FPS))
        while True:
            ret, img = video_capture.read()
            if ret:
                cv2.imshow("img", img)

app = wx.App(False)
frame = GUI.GUI(None)
frame.Show(True)
frame.setDriverScore(100)
app.MainLoop()
