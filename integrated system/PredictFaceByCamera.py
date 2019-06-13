# -*- coding: UTF-8 -*-

import cv2
import numpy as np
import CNNMODEL as cnn


# Constants
EMOTION_LABELS = ['angry', "disgust", 'fear', 'happy', 'sad', 'surprise', 'neutral']
CASC_PATH = "./resources/chaarcascade_frontalface_default.xml"


def predict_emotion(face_image_gray, cnn_model):  # a single cropped face
    resized_img = cv2.resize(face_image_gray, (48, 48), interpolation=cv2.INTER_AREA)
    pixel = np.zeros((48, 48))
    for i in range(48):
        for j in range(48):
            pixel[i][j] = resized_img[i][j]
    list = cnn_model.predict(pixel)

    return list


def main():
    faceCascade = cv2.CascadeClassifier(CASC_PATH)

    # Load the model
    cnn_model = cnn.CNNModel()

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
        for (x, y, w, h) in faces:
            face_image_gray = img_gray[y:y + h, x:x + w]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            list2 = predict_emotion(face_image_gray, cnn_model)
            print(EMOTION_LABELS[np.argmax(list2)])

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # character q means exit
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
