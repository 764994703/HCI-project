import cv2

import numpy as np

import math

import time
 
def rgbtohsi1(rgb_lwpImg):
    rows = int(rgb_lwpImg.shape[0])
    cols = int(rgb_lwpImg.shape[1])
    b, g, r = cv2.split(rgb_lwpImg)
    # 归一化到[0,1]
    b = b / 255.0
    g = g / 255.0
    r = r / 255.0
    hsi_lwpImg = rgb_lwpImg.copy()
    H, S, I = cv2.split(hsi_lwpImg)
    for i in range(rows):
        for j in range(cols):
            #num = 0.5 * ((r[i, j]-g[i, j])+(r[i, j]-b[i, j]))
            #den = np.sqrt((r[i, j]-g[i, j])**2+(r[i, j]-b[i, j])*(g[i, j]-b[i, j]))
            #theta = float(np.arccos(num/den))

            #min_RGB = min(min(b[i, j], g[i, j]), r[i, j])
            sum = b[i, j]+g[i, j]+r[i, j]
            
            I = sum/3.0
            # 输出HSI图像，扩充到255以方便显示，一般H分量在[0,2pi]之间，S和I在[0,1]之间
            #hsi_lwpImg[i, j, 0] = H*255
            #hsi_lwpImg[i, j, 1] = S*255
            hsi_lwpImg[i, j, 2] = I*255
    return hsi_lwpImg

        
def hsitorgb(hsi_img):

    h = int(hsi_img.shape[0])

    w = int(hsi_img.shape[1])

    H, S, I = cv2.split(hsi_img)

    H = H / 255.0

    S = S / 255.0

    I = I / 255.0

    bgr_img = hsi_img.copy()

    B, G, R = cv2.split(bgr_img)

    for i in range(h):

        for j in range(w):

            if S[i, j] < 1e-6:

                R = I[i, j]

                G = I[i, j]

                B = I[i, j]

            else:

                H[i, j] *= 360

                if H[i, j] > 0 and H[i, j] <= 120:

                    B = I[i, j] * (1 - S[i, j])

                    R = I[i, j] * (1 + (S[i, j] * math.cos(H[i, j]*math.pi/180)) / math.cos((60 - H[i, j])*math.pi/180))

                    G = 3 * I[i, j] - (R + B)

                elif H[i, j] > 120 and H[i, j] <= 240:

                    H[i, j] = H[i, j] - 120

                    R = I[i, j] * (1 - S[i, j])

                    G = I[i, j] * (1 + (S[i, j] * math.cos(H[i, j]*math.pi/180)) / math.cos((60 - H[i, j])*math.pi/180))

                    B = 3 * I[i, j] - (R + G)

                elif H[i, j] > 240 and H[i, j] <= 360:

                    H[i, j] = H[i, j] - 240

                    G = I[i, j] * (1 - S[i, j])

                    B = I[i, j] * (1 + (S[i, j] * math.cos(H[i, j]*math.pi/180)) / math.cos((60 - H[i, j])*math.pi/180))

                    R = 3 * I[i, j] - (G + B)

            bgr_img[i, j, 0] = B * 255

            bgr_img[i, j, 1] = G * 255

            bgr_img[i, j, 2] = R * 255

    return bgr_img


img = cv2.imread("C:/Users/hasee/Desktop/skin-python/testinput/test3.jpg")
i = 0
time1 = time.time()
while i < 10:
    i += 1
    img1 = rgbtohsi1(img)

print(time.time() - time1)
cv2.imshow('img1', img1)
