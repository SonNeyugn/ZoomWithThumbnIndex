import pyautogui as pa

import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL


################################
wCam, hCam = 640, 480
################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon = 0.8)

scroll = 0
length_old = 0
length_new = 0

# volume.GetMute()
# volume.GetMasterVolumeLevel()

while True:
    length_old = length_new
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        z = lmList[1][3]
        #print("x1 position:", x1)
        #print("y1 position:", y1)
        #print("z position:", z)

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length_new = math.hypot(x2 - x1, y2 - y1)
        # print(length)
        d_change = length_new - length_old
        scroll = int(d_change * 100)
        #print("Scroll value: ", scroll)
        #print("d_change: ", d_change)
        #print("distance: ", z)

        if (((d_change < -5) or (d_change > 5)) ):
            pa.keyDown("ctrl")
            pa.scroll(scroll)
        elif ((-5 < d_change) and (d_change < 5)) :
            pa.keyUp("ctrl")

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)