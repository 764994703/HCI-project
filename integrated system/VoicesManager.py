# -*- coding: UTF-8 -*-

import pyttsx3
import pygame
import random
import time
import os
import win32com
from PlayMp3 import PlayMp3


VOICES_PATH = "./voices/"
ALARM_ANGRY_JOKE_NUM = 7
ALARM_ANGRY_MUSIC_NUM = 1

ALARM_ANGRY_TIME_GAP = 10  # second
ALARM_SLEEPY_TIME_GAP = 1
INFORM_NO_EYES_TIME_GAP = 1800  # = 30 minute
INFORM_NO_FACE_TIME_GAP = 1800

class VoicesManager:
    def __init__(self):
        self.playmp3 = PlayMp3()
        self.alarm_angry_joke_index = 0
        self.alarm_angry_music_index = 0
        self.param_config = None
        self.last_time_alarm_sleepy = 0
        self.last_time_alarm_angry = 0
        self.last_time_inform_status = 0
        self.last_time_inform_noeyes = 0
        self.last_time_inform_noface = 0

    def setParamConfig(self, param_config):
        self.param_config = param_config

    def alarmSleepy(self):
        cur_time = time.time()
        if cur_time - self.last_time_alarm_sleepy <= ALARM_SLEEPY_TIME_GAP:
            return
        self.last_time_alarm_sleepy = cur_time

        file_path = VOICES_PATH + "sleepy.mp3"
        self.playmp3.emergentplay(file_path)

    def alarmAngry(self):
        cur_time = time.time()
        if cur_time - self.last_time_alarm_angry <= ALARM_ANGRY_TIME_GAP:
            return
        self.last_time_alarm_angry = cur_time

        mode = self.param_config.getAngryAlarmMode()
        file_path = VOICES_PATH
        if mode == 0:
            file_path += "joke/joke%d.wav" % self.alarm_angry_joke_index
            self.alarm_angry_joke_index = (self.alarm_angry_joke_index + 1) % ALARM_ANGRY_JOKE_NUM
        else:
            file_path += "music/music%d.wav" % self.alarm_angry_music_index
            self.alarm_angry_music_index = (self.alarm_angry_music_index + 1) % ALARM_ANGRY_MUSIC_NUM
        self.playmp3.emergentplay(file_path)

    # @param risk_level:0 is fine and 2 is in danger
    def informStatus(self, risk_level):
        cur_time = time.time()
        if cur_time - self.last_time_inform_status <= self.param_config.getDriverStatusInformGap() * 60:
            return
        self.last_time_inform_status = cur_time

        file_path = VOICES_PATH
        if risk_level == 0:
            return
        elif risk_level == 1:
            file_path += "status-middlerisk.wav"
        else:
            file_path += "status-highrisk.wav"

        self.playmp3.play(file_path)

    def informNoEyes(self):
        cur_time = time.time()
        if cur_time - self.last_time_inform_noeyes <= INFORM_NO_EYES_TIME_GAP:
            return
        self.last_time_inform_noeyes = cur_time

        file_path = VOICES_PATH + "noEyes.wav"
        self.playmp3.play(file_path)

    def informNoFace(self):
        cur_time = time.time()
        if cur_time - self.last_time_inform_noface <= INFORM_NO_FACE_TIME_GAP:
            return
        self.last_time_inform_noface = cur_time

        file_path = VOICES_PATH + "noFace.wav"
        self.playmp3.play(file_path)


def readscore(score):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for item in voices:
        print(item.id, item.languages)
    engine.setProperty("voice", "HKEY_LOCAL_MACHINE/SOFTWARE/Microsoft/Speech/Voices/Tokens/TTS_MS_ZH-CN_HUIHUI_11.0")
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 15)
    engine.say(str(score) + "分")
    engine.runAndWait()


def randomplay(mode):
    if (mode == 0):
        rootdir = "./voices/joke"
    elif (mode == 1):
        rootdir = "./voices/sketch"
    elif (mode == 2):
        rootdir = "./voices/music"
    else:
        print("error")
    file_names = []
    for parent, dirnames, filenames in os.walk(rootdir):
        file_names = filenames
    x = random.randint(0, len(file_names) - 1)
    file = "./voices/joke/" + file_names[x]
    print(file)
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
