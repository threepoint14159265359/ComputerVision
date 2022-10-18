import random as ran
import cv2
from HandDetector import *
from time import sleep
from CvSnakeGame import *


game = Snake()



## video capture
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

## hand detection 
hand_detector = HandDetector(detectionCon=0.3, maxHands=1)



## frame to frame reading of the video 
while True:
    success, img = cap.read() ## read the capture  of each frame 
    img.flags.writeable = False 
    img = cv2.flip(img,1) ##if we look in a mirror, it's intuition is non-intuitive
    img = hand_detector.find_hands(img) ## find the hands in the current frame 

    ##play ground
    cv2.rectangle(img, (0,0), (1280,720), (0,0,0), cv2.FILLED)

    ## check if the hand is detected and extract the frist one 

    lmList =  hand_detector.find_landmarks_pos(img=img, draw=False) #landMarks list
    index_finger = hand_detector.get_index_finger_landmark()
    print(index_finger)
    cv2.circle(img, index_finger, 20, (200, 0, 200), cv2.FILLED) # draw index finger_finger = lmList[8][0:2] ## the first values are the nth joint in the hand, and the second number is the x,y,z coordinates in a plane and since we don't need the second one. So, we'll only register the x,y (2-d) plane
    cv2.circle(img, index_finger, 20, (200, 0, 200), cv2.FILLED) # draw index finger
    if index_finger != None:
        img = game.update(img, index_finger)
        sleep(0.025)

    cv2.imshow("Snake", img)
    cv2.waitKey(1)