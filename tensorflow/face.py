import cv2
import sys
import time
import numpy as np
import CNN_MODEL as cnn

emotion_labels = ['angry', "disgust", 'fear', 'happy', 'sad', 'surprise', 'neutral']
cascPath = ".\haarcascade_frontalface_default.xml"


def predict_emotion(face_image_gray):  # a single cropped face
    resized_img = cv2.resize(face_image_gray, (48, 48), interpolation=cv2.INTER_AREA)
    # cv2.imwrite(str(index)+'.png', resized_img)
    # image = resized_img.reshape(1, 1, 48, 48)
    pixel = np.zeros((48, 48))
    for i in range(48):
        for j in range(48):
            pixel[i][j] = resized_img[i][j]
    list = cnn.Predict(pixel, sess)

    return list

# def main():
faceCascade = cv2.CascadeClassifier(cascPath)

# load the model
sess = cnn.Initialize()

last_time = 0
video_capture = cv2.VideoCapture(0) # 0为默认摄像头
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, 1)

    faces = faceCascade.detectMultiScale(
        img_gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    counter = 0
    for (x, y, w, h) in faces:
        face_image_gray = img_gray[y:y + h, x:x + w]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        list2 = predict_emotion(face_image_gray)
        curTime = time.time()
        if last_time != 0:
            print("time consumed:%f" %(curTime - last_time))
        last_time = curTime
        # print(emotion_labels[np.argmax(list2)])

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # character q means exit
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
