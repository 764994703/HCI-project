from imutils import face_utils
from scipy.spatial import distance as dist
import numpy as np
import argparse
import imutils
import dlib
import cv2
import time

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("C:/Users/hasee/Desktop/hci-python/shape_predictor_68_face_landmarks.dat")
facetrace = (0,0,0,0)

def rect_to_bb(rect):
	# take a bounding predicted by dlib and convert it
	# to the format (x, y, w, h) as we would normally do
	# with OpenCV
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
 
	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)
 
	# return the eye aspect ratio
	return ear

if __name__ == '__main__':
    aspectlist = []
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    # load the input image, resize it, and convert it to grayscale
    video_capture = cv2.VideoCapture(0) # 0为默认摄像头
    time1 = time.time()
    j = 0
    while True:
            # Capture frame-by-frame
            et, image = video_capture.read()
            #image = imutils.resize(image, width=350)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
             
            # detect faces in the grayscale image
            rects = detector(gray, 1)
            # loop over the face detections
            for (i, rect) in enumerate(rects):
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                    #facetrace = rect_to_bb(rect)
                for (x, y) in shape:
                    cv2.circle(image, (x, y), 1, (0, 0, 255), -1)
                cv2.rectangle(image, (facetrace[0], facetrace[1]), (facetrace[0] + facetrace[2], facetrace[1] + facetrace[3]), (0, 255, 0), 2)
	
                leftEye = shape[lStart:lEnd] 
                rightEye = shape[rStart:rEnd]
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
                ear = (leftEAR + rightEAR)/2
                aspectlist.append(round(ear,4))
                #print(round(ear,4))
		# average the eye aspect ratio together for both eyes
		#ear = (leftEAR + rightEAR)/2.0
		# show the output image with the face detections + facial landmarks
            cv2.imshow("Output", image)
            if(j % 50 == 0):
                print(len(aspectlist) / (time.time() - time1))
                time1 = time.time()
                print(aspectlist)
                aspectlist = []
            j += 1
            cv2.waitKey(1)
#image = cv2.imread("C:/Users/hasee/Desktop/skin-python/testinput/test3.jpg")
