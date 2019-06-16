import numpy as np
import cv2 as cv
import time
import imutils

lastvalidface = (1,1,1,1)
lastvalideyes = (1,1,1,1)
tracecnt = 0            #face trace
covercnt = 0            #eye detect fails

gamma = 0.8
table = np.array([((i / 255.0) ** gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")


face_cascade = cv.CascadeClassifier('./haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('./haarcascade_eye_tree_eyeglasses.xml')

def eyecenters(img):
    global lastvalidface
    global lastvalideyes
    global tracecnt
    global covercnt
    eyecenterlist = []

    ret = 0                 #0:OK -1:cover eyes -2:can't find face
    
    tracemax = 90
    
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.equalizeHist(gray)


    faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize = (100,100))
    eyes = []
    if(len(faces) == 0 and tracecnt <= tracemax):
        (x,y,w,h) = lastvalidface
        facex = x
        facey = y
        cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        tracecnt += 1
        #roi_gray = gray[y:y+h, x:x+w]
        #roi_color = img[y:y+h, x:x+w]
        #eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 8, minSize = (10,10))
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 8, minSize = (5,5))
        if(len(eyes) != 0):
            for (ex,ey,ew,eh) in eyes:
                lastvalideyes = (ex,ey,ew,eh)
                eyecenterlist.append((facex + ex + ew/2, facey + ey + eh/2))
                cv.circle(img, (int(facex + ex + ew/2), int(facey + ey + eh/2)), 20, (0,255,0),2)
                #cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            covercnt = 0
        else:
            covercnt += 1
            if(covercnt > tracemax):
                ret = -1

    elif(len(faces) == 0 and tracecnt > tracemax):
        ret = -2
    else:
        (x,y,w,h) = faces[0]
        lastvalidface = (x,y,w,h)
        facex = x
        facey = y
        cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        tracecnt = 0
        
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 8, minSize = (5,5))
        if(len(eyes) != 0):
            for (ex,ey,ew,eh) in eyes:
                lastvalideyes = (ex,ey,ew,eh)
                eyecenterlist.append((facex + ex + ew/2, facey + ey + eh/2))
                cv.circle(img, (int(facex + ex + ew/2), int(facey + ey + eh/2)), 20, (0,255,0),2)
                #cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            covercnt = 0
        else:
            covercnt += 1
            if(covercnt > tracemax):
                ret = -1
        #for each in eyecenterlist:
        #    cv.circle(img, (int(each[0]), int(each[1])), 20, (0,255,0),2)
    
    #out.write(img)
    cv.imshow('img',img)
    return ret

if __name__ == '__main__':
    #fourcc = cv.VideoWriter_fourcc('I', '4', '2', '0')
    #out = cv.VideoWriter("C:/Users/hasee/Desktop/skin-python/testvidios/output.avi",fourcc, 5.0, (640,480))
    
    video_capture = cv.VideoCapture(0) # 0为默认摄像头
    k = 0
    timestart = time.time()
    cnt = 0
    #img = cv.imread("C:/Users/hasee/Desktop/skin-python/testinput/test4.jpg")
    #img = imutils.resize(img, width=640)
    #eyecenters(img)
    while True:
        # Capture frame-by-frame
        et, img = video_capture.read()
        img = imutils.resize(img, width=640)
        
        #if(k % 10 == 0):
        ret = eyecenters(img)
        print(ret)
        #k = k + 1
        cv.waitKey(1)
        
        cnt += 1
        if(time.time() - timestart > 1):
            timestart = time.time()
            print(cnt)
            cnt = 0
            
#img = cv.imread("C:/Users/hasee/Desktop/skin-python/testinput/test3.jpg")


    

