import cv2
import numpy as np
import HandTrackingModule as htm
import time as t
import pyautogui as p
import autopy



wCam, hCam = 640, 480
frameR = 100
smoothening = 7


pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
# print(wScr, hScr)
downF=False
while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(255, 0, 255), 2)
        # 4. Only Index Finger : Moving Mode
        if fingers[0]==0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4]==0:
            if not downF:
                downF=True
                p.mouseDown()
            x1,y1=lmList[10][1:]
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7. Move Mouse
            p.moveTo(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:

            l1, img, lineInfo = detector.findDistance(8, 12, img)
            l2, img, lineInfo = detector.findDistance(12, 16, img)
            length = l1 + l2
            # print(l2)
            if l2 < 40:
                autopy.mouse.click(autopy.mouse.Button.RIGHT)
        if fingers[0]==1 and fingers[1]:
            l,img,lineInfo = detector.findDistance(4,8,img)
            if l<40:
                p.scroll(-20)
            else:
                p.scroll(20)
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. Convert Coordinates

            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            if downF:
                downF = False
                p.moveTo(wScr - clocX, clocY)
                p.mouseUp(button='left',x=wScr-clocX,y=clocY)

            # 7. Move Mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 8. Both Index and middle fingers are up : Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)
            # 10. Click mouse if distance short
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()


    cv2.imshow("Image", img)
    key = cv2.waitKey(10)
    if key==27:
        break
