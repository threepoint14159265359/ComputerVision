import random as ran
import cv2
from HandDetector import *
from time import sleep
from CvSnakeGame import *
from GUI import Button
from CONSTS import *


game = Snake()




## video capture
cap = cv2.VideoCapture(0)
cap.set(3, WIDTH)
cap.set(4, HEIGHT)

## hand detection 
hand_detector = HandDetector(detectionCon=0.3, maxHands=1)


## frame to frame reading of the video 
while True:
    _, img = cap.read() ## read the capture  of each frame 
    img.flags.writeable = False 
    img = cv2.flip(img,1) ##if we look in a mirror, it's intuition is non-intuitive
    

    ##Make the back-ground black
    #img = cv2.rectangle(img, (0,0), (WIDTH,HEIGHT), (0,0,0), cv2.FILLED)
    

    ### CREATE SOME BUTTONS FOR THE MENU 
    """
    start_button = Button(img,  int(WIDTH/3), int(HEIGHT/7), 2* int(WIDTH/3), int((1.5)*(HEIGHT/7)), ( 255,0,0), "Start")
    game_mode_button = Button(img,  int(WIDTH/3), int(HEIGHT/4), 2* int(WIDTH/3), int((1.3)*(HEIGHT/4)), ( 255,0,0), "Mode")
    help_button = Button(img,  int(WIDTH/3), int(HEIGHT/2.8), 2* int(WIDTH/3), int((1.21)*(HEIGHT/2.8)), ( 255,0,0), "Help")
    settings_button = Button(img,  int(WIDTH/3), int(HEIGHT/2.15), 2* int(WIDTH/3), int((1.15)*(HEIGHT/2.15)), ( 255,0,0), "Settings")
    quit_button = Button(img,  int(WIDTH/3), int(HEIGHT/1.76), 2* int(WIDTH/3), int((1.13)*(HEIGHT/1.76)) ,  ( 255,0,0), "Quit")

    """
    
    
    
    ### FROM HERE ONE --- THE MAIN GAME STARTS.
    img = hand_detector.find_hands(img, draw = False) ## read the hand
    
    cv2.rectangle(img, (0,0), (1280,720), (0,0,0), cv2.FILLED) ### fill the screen black 
    
    lmList =  hand_detector.find_landmarks_pos(img=img, draw=False) #extract landmarks
    index_finger = hand_detector.get_index_finger_landmark() # extract index finer from landmarks

    if index_finger != None:
        #print(index_finger)
        cv2.circle(img, index_finger, 20, (200, 0, 200), cv2.FILLED) # draw index finger
        img = game.update(img, index_finger)
        sleep(0.025)



    cv2.imshow("Snake", img)
    # cv2.setMouseCallback("Snake", game_mode_button.hover)
    # cv2.setMouseCallback("Snake", help_button.hover)
    # cv2.setMouseCallback("Snake", settings_button.hover)
    # cv2.setMouseCallback("Snake", quit_button.hover)

    cv2.waitKey(1)




