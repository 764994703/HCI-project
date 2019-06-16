# -*- coding: UTF-8 -*-

from GUI import GUI
from AngryPredictModel import AngryPredictModel
from TiredPredictModel import TiredPredictModel
from VoicesManager import VoicesManager

import time
import math
import threading
import wx
import os
import numpy as np
import cv2
from imutils import face_utils
from scipy.spatial import distance as dist
import dlib
import copy


VIDEO_PATH = 0  # 0为默认摄像头
SHOW_PICTURE = True
RESOURCES_PATH = "./resources/"
DRIVING_SPEED = 5  # km/h
TIME_WINDOW_SIZE = 10  # 秒
ANGRY_TIME = 3  # 秒
TRACE_MAX = 90  # 连续TRACE_MAX帧识别不到面部就会报错
SKIP_FRAME = 1  # 每SKIP_FRAME帧取1帧分析

ANGRY = 0  # index in EMOTION_LABELS
EMOTION_LABELS = ['angry', "disgust", 'fear', 'happy', 'sad', 'surprise', 'neutral']

face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./haarcascade_eye_tree_eyeglasses.xml')
predictor = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")

lastvalidface = (1, 1, 1, 1)
tracecnt = 0  # face trace
covercnt = 0  # eye detect fails
detector = dlib.get_frontal_face_detector()
facetrace = (0, 0, 0, 0)
reportscore = [1]


# @return 0: OK, -1: cover eyes, -2: can't find face
def get_face_bound(img):
    global lastvalidface
    global tracecnt
    global covercnt

    gray = img
    faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(100, 100))

    if len(faces) == 0 and tracecnt <= TRACE_MAX:
        (x, y, w, h) = lastvalidface
        facex = x
        facey = y
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        tracecnt += 1

        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 8, minSize=(3, 3))
        if len(eyes) != 0:
            for (ex, ey, ew, eh) in eyes:
                cv2.circle(img, (int(facex + ex + ew / 2), int(facey + ey + eh / 2)), 20, (255, 0, 0), 2)
                covercnt = 0
        else:
            covercnt += 1
            if covercnt > TRACE_MAX:
                cv2.imshow('img', img)
                return -1

    elif len(faces) == 0 and tracecnt > TRACE_MAX:
        cv2.imshow('img', img)
        return -2
    else:
        (x, y, w, h) = faces[0]
        lastvalidface = (x, y, w, h)
        facex = x
        facey = y
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        tracecnt = 0

        roi_gray = gray[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 8, minSize=(3, 3))
        if (len(eyes) != 0):
            covercnt = 0
            for (ex, ey, ew, eh) in eyes:
                cv2.circle(img, (int(facex + ex + ew / 2), int(facey + ey + eh / 2)), 20, (255, 0, 0), 2)

        else:
            covercnt += 1
            if (covercnt > TRACE_MAX):
                ret = -1
    ret = (x, y, x + w, y + h)
    if SHOW_PICTURE:
        cv2.imshow('img', img)
    return ret


class ParamConfig:
    def __init__(self):
        self.enable_angry_detect = True
        self.enable_angry_detect_lock = threading.Lock()
        self.angry_alarm_mode = 0  # 0 for joke, 1 for music
        self.angry_alarm_mode_lock = threading.Lock()
        self.driver_status_inform_gap = 5  # minutes
        self.driver_status_inform_gap_lock = threading.Lock()

    def setEnableAngryDetect(self, value):
        self.enable_angry_detect_lock.acquire()
        self.enable_angry_detect = value
        print("Enable angry detect: %r" % value)
        self.enable_angry_detect_lock.release()

    def getEnableAngryDetect(self):
        self.enable_angry_detect_lock.acquire()
        ret = copy.copy(self.enable_angry_detect)
        self.enable_angry_detect_lock.release()
        return ret

    def setAngryAlarmMode(self, mode):
        self.angry_alarm_mode_lock.acquire()
        self.angry_alarm_mode = mode
        print("Angry alarm mode: %d" % mode)
        self.angry_alarm_mode_lock.release()

    def getAngryAlarmMode(self):
        self.angry_alarm_mode_lock.acquire()
        mode = copy.copy(self.angry_alarm_mode)
        self.angry_alarm_mode_lock.release()
        return mode

    def setDriverStatusInformGap(self, gap):
        self.driver_status_inform_gap_lock.acquire()
        self.driver_status_inform_gap = gap
        print("Driver status inform gap: %d" % gap)
        self.driver_status_inform_gap_lock.release()

    def getDriverStatusInformGap(self):
        self.driver_status_inform_gap_lock.acquire()
        gap = copy.copy(self.driver_status_inform_gap)
        self.driver_status_inform_gap_lock.release()
        return gap


MIN_DRIVER_SCORE = 0
MAX_DRIVER_SCORE = 100
SCORE_DEC_VEL = 1
TURNS_FOR_INC = 3
SCORE_INC_VEL = 0.5
SCORE_INC_COLD_DOWN = 2

class TiredEstimatingModel:
    def __init__(self):
        self.driver_score = MAX_DRIVER_SCORE
        self.not_tired_turn_counter = 0
        self.restore_turn_counter = 0

    def getScore(self):
        return self.driver_score

    def input(self, is_tired):
        if is_tired:
            self.not_tired_turn_counter = 0
            self.restore_turn_counter = 0

            self.driver_score -= SCORE_DEC_VEL
            if self.driver_score < MIN_DRIVER_SCORE:
                self.driver_score = MIN_DRIVER_SCORE
        elif self.not_tired_turn_counter == TURNS_FOR_INC:
            self.restore_turn_counter += 1
            if self.restore_turn_counter == SCORE_INC_COLD_DOWN:
                self.restore_turn_counter = 0
                self.driver_score += 1
                if self.driver_score > MAX_DRIVER_SCORE:
                    self.driver_score = MAX_DRIVER_SCORE
        else:
            self.not_tired_turn_counter += 1



class CMThread(threading.Thread):
    def __init__(self, gui):
        threading.Thread.__init__(self)

        # Common Variables
        self.now_speed = 30
        self.timer = 0
        self.param_config = ParamConfig()

        # Components
        self.gui = gui
        self.vm = VoicesManager()
        self.vm.setParamConfig(self.param_config)
        self.tem = TiredEstimatingModel()
        self.tpm = TiredPredictModel()
        self.apm = AngryPredictModel()

        # Special Case Variables
        self.no_face_fnum = 0
        self.no_eyes_fnum = 0

        # Models' Variables
        #   - Angry Estimating Model
        self.time_win = []
        for i in range(TIME_WINDOW_SIZE):  # initialize time window
            self.time_win.append(0)
        self.is_angry_time_win = []
        for i in range(TIME_WINDOW_SIZE):  # initialize time window
            self.is_angry_time_win.append(0)
        self.time_win_index = 0
        self.time_counter = 0
        #   - Tired Estimating Model
        self.is_tired = False
        self.medians = [0.25]
        self.eye_ear = [0.25]

    def printLog(self, string):
        print("time %d :" % self.timer + string)

    # Main function
    def run(self):
        video_capture = cv2.VideoCapture(VIDEO_PATH)
        VIDEO_FPS = math.ceil(video_capture.get(cv2.CAP_PROP_FPS))
        print("FPS: " + str(VIDEO_FPS))
        frame_counter = 0
        valid_frame_counter = 0
        while True:
            frame_counter += 1

            # If not driving
            if self.now_speed < DRIVING_SPEED:
                video_capture.read()
                continue

            ret, img = video_capture.read()
            if frame_counter % SKIP_FRAME == 0 and ret:
                valid_frame_counter += 1
                img_copy = copy.copy(img)

                # Pre-process
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)

                # Get face bound
                fb_points = get_face_bound(gray)
                cv2.waitKey(1)  # delay to show picture

                # Check if losing face or eyes
                if fb_points == -2:
                    self.no_face_fnum += 1
                elif fb_points == -1:
                    self.no_eyes_fnum += 1
                else:
                    face_bound = dlib.rectangle(int(fb_points[0]), int(fb_points[1]), int(fb_points[2]), int(fb_points[3]))

                    # Predict tired
                    ret = self.tpm.predict(gray, face_bound)
                    if ret != 0:
                        self.eye_ear.append(round(ret, 4))
                    # Predict angry
                    if self.param_config.getEnableAngryDetect():
                        if self.apm.predict(img_copy):
                            self.time_win[self.time_win_index] += 1

                # 1 second pass
                if frame_counter == VIDEO_FPS:
                    frame_counter = 0
                    self.timer += 1

                    # Special case
                    if self.no_eyes_fnum >= valid_frame_counter / 2:
                        self.vm.informNoEyes()
                        self.printLog("can't recognize eyes")
                    if self.no_face_fnum >= valid_frame_counter / 2:
                        self.vm.informNoFace()
                        self.printLog("can't recognize face")
                    self.no_eyes_fnum = 0
                    self.no_face_fnum = 0

                    # Tired Estimating Model
                    if self.eye_ear != []:
                        median = np.median(self.eye_ear)
                        longtermmedian = np.median(self.medians)
                        if median / longtermmedian < 0.7:  # 1.8 / 2.8 = 0.64
                            self.printLog("driver is sleeping!")
                            self.vm.alarmSleepy()
                        if median / longtermmedian < 0.90:
                            # The driver is tired at this second
                            self.printLog("driver is tired!")
                            self.tem.input(True)
                        else:
                            self.tem.input(False)
                        if len(self.medians) < 3:
                            self.medians.append(median)

                        # print("当前眼高宽比：" + str(median))
                        # print("基准眼高宽比：" + str(longtermmedian))
                        self.eye_ear = []

                    # Angry Estimating Model
                    if self.time_win[self.time_win_index] >= valid_frame_counter / 6:
                        self.is_angry_time_win[self.time_win_index] = 1
                    else:
                        self.is_angry_time_win[self.time_win_index] = 0
                    self.time_win_index = (self.time_win_index + 1) % TIME_WINDOW_SIZE
                    self.time_win[self.time_win_index] = 0
                    if self.param_config.getEnableAngryDetect() and sum(self.is_angry_time_win) >= ANGRY_TIME:
                        self.vm.alarmAngry()
                        self.printLog("driver is angry!")

                    # Update driver's score in GUI
                    driver_score = self.tem.getScore()
                    # Inform driver of status
                    self.gui.setDriverScore(driver_score)
                    if driver_score < 60:
                        self.vm.informStatus(2)
                    elif driver_score < 80:
                        self.vm.informStatus(1)

                    valid_frame_counter = 0

                # Quit
                if False:
                    break

        video_capture.release()
        cv2.destroyAllWindows()


def main():
    # Close TF's logging
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    # Init GUI
    app = wx.App(False)
    frame = GUI(None)
    frame.Show(True)

    # Start main thread
    cm_thread = CMThread(frame)
    cm_thread.start()

    # Set Configurer
    frame.setParamConfig(cm_thread.param_config)

    # Start GUI
    app.MainLoop()


if __name__ == "__main__":
    main()
