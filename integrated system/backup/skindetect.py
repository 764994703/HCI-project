import cv2
import numpy as np
    
def skindetect(frame):
    #frame=cv2.GaussianBlur(frame,(5,5),0)
    yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    sp = yuv.shape
    height = sp[0]
    width = sp[1]
    #print(height ,":" , width , "\n")
    beginx = 5000
    beginy = 5000
    endx = 0
    endy = 0
    mask = np.zeros((height, width), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            cr = yuv.item(i, j, 1)
            cb = yuv.item(i, j, 2)
            if( 3 < cr and cr < 173 and cb > 77 and cb < 127):
                mask[i ,j] = 1
                if (beginx > i):
                    beginx = i
                if (beginy > j):
                    beginy = j
                if (endx < i):
                    endx = i
                if (endy < j):
                    endy = j
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    output = cv2.bitwise_and(frame, frame, mask = mask)
    #mask = mask & frame
    y = beginx
    x = beginy
    h = endx - beginx
    w = endy - beginy
    
    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("detected", output)
    
if __name__ == '__main__':
    last_time = 0
    video_capture = cv2.VideoCapture(0) # 0为默认摄像头
    while True:
        # Capture frame-by-frame
        et, frame = video_capture.read()
        skindetect(frame)
        cv2.waitKey(100)
        
    #img = cv2.imread("C://Users/hasee/Desktop/skin-python/testinput/test1.jpg")
    #skindetect(img)
    #cv2.waitKey(1)
    


