import mediapipe as mp
import numpy as np
import cv2
import time
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
print(volume.GetVolumeRange())
#volume.SetMasterVolumeLevel(0, None)
minVol = volume.GetVolumeRange()[0]
maxVol = volume.GetVolumeRange()[1]


while True:
    success,img = cap.read()
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results =  hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for ID, lm in enumerate(handLms.landmark):
                h,w,c = img.shape
                cx,cy= int(lm.x*w), int(lm.y*h)
                #print(ID, cx, cy)
                if ID == 4:
                    cv2.circle(img,(cx,cy),10,(0,0,0),cv2.FILLED)
                    x1, y1 = cx, cy
                    #print(str(x1) + ',' + str(y1))
                if ID == 8:
                    cv2.circle(img,(cx,cy),10,(0,0,0),cv2.FILLED)
                    x2, y2 = cx, cy
                    #print(str(x2) + ',' + str(y2))
            cv2.line(img, (x1,y1), (x2,y2), (0,0,0), 3)
            length = math.hypot(x2-x1, y2-y1)
            #print(str(length))
            vol = np.interp(length, [20,200], [minVol, maxVol])
            print(vol)
            volume.SetMasterVolumeLevel(vol, None)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 3 )        
    cv2.namedWindow("Video", cv2.WINDOW_NORMAL) 
    cv2.resizeWindow("Video", 640, 480) 
    cv2.imshow("Video", img)
    
    if cv2.waitKey(20) & 0xFF==ord('d'):
        break

cv2.destroyAllWindows()