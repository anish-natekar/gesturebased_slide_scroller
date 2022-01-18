import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
######
wCam, hCam = 640, 480
frameR = 100 # frame Reduction
smoothening = 3
######
click = True
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
loop = True
slide = True

cap = cv2.VideoCapture(0)
cap.set(3, wCam) # width is 3
cap.set(4, hCam) # height is 4
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
while loop:
    # 1. Find the hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # 2. Get the tip of the index and middle fingers
    if len(lmList)!=0:
        # index finger tip
        x1, y1 = lmList[8][1:]
        # middle finger tip
        x2, y2 = lmList[12][1:]

    # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), (255,0,255), 2)
    # 4. Only Index Finger : Moving Mode
        if slide == False and fingers[1] ==0 and fingers[2] == 0 and fingers[0] == 0:
            slide = True
            print("slide enabled again")
        if fingers[1] == 1 and fingers[0] == 0 and fingers[2] == 0:
            
        # 5. Convert our coordinates
            
            x3 = np.interp(x1, (frameR, wCam-frameR), (0,wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

    # 6. Smoothen Values
            clocX = plocX +(x3-plocX)/smoothening
            clocY = plocY +(y3-plocY)/smoothening
    # 7. Move Mouse
            # wScr - x3 flips the mouse direction horizontally
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
    # 8. Both Index and Middle fingers are up : Clicking Mode
        if fingers[1] == 1 and slide:
            if fingers[2] == 1:
                print("middle")
                autopy.key.tap(autopy.key.Code.RIGHT_ARROW)
            elif fingers[0] == 1:
                print("thumb")
                autopy.key.tap(autopy.key.Code.LEFT_ARROW)
            slide = False       
    # Exit loop using pinky finger
        if fingers[4] == 1 and fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0:
            loop = False
            print("Exiting loop")                   
    # PROTOTYPE by Anish Natekar
    # 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)