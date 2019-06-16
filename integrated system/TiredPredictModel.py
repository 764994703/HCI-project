# -*- coding: UTF-8 -*-

import cv2
from imutils import face_utils
from scipy.spatial import distance as dist
import dlib

RESOURCES_PATH = "./resources/"
lastvalidface = (1, 1, 1, 1)
tracecnt = 0  # face trace
covercnt = 0  # eye detect fails
detector = dlib.get_frontal_face_detector()
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./haarcascade_eye_tree_eyeglasses.xml')
predictor = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")
facetrace = (0, 0, 0, 0)
reportscore = [1]


def rect_to_bb(rect):
    # take a bounding predicted by dlib and convert it
    # to the format (x, y, w, h) as we would normally do
    # with Opencv2
    x = int(rect.left() * 0.3)
    y = int(rect.top() * 0.3)
    w = int((rect.right() - x) * 2)
    h = int((rect.bottom() - y) * 2)

    # return a tuple of (x, y, w, h)
    return (x, y, w, h)


def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])
    if (C == 0):
        return 0
    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear


def get_eye_ear(gray, rect):
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    # determine the facial landmarks for the face region, then
    # convert the facial landmark (x, y)-coordinates to a NumPy
    # array
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)
    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]
    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)
    ear = (leftEAR + rightEAR) / 2
    return ear


class TiredPredictModel:
    def __init__(self):
        pass

    def predict(self, gray, face_bound):
        return get_eye_ear(gray, face_bound)
