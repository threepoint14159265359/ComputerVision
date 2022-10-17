
import random as ran
import cv2
from HandDetector import *
from time import sleep

class Snake:
    def __init__(self) -> None:
        self.points = [] # all points of the snake 
        self.lengths = [] # distance between each point 
        self.current_length = 0 ## total length of the snake 
        self.allowed_length = 100 ## total allowed length 
        self.previous_head = 0, 0 # previous head point
        self.foodx = 0
        self.foody = 0
        self.randomizeFood() 
        self.game_over = False
        self.score = 0 
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def randomizeFood(self):
        self.foodx, self.foody = ran.randint(100,1100), ran.randint(100,600)
        if (self.foodx, self.foody) in self.points:
            self.randomizeFood()


    def update(self, imgMain, currentHead):
        px, py = self.previous_head
        cx, cy = currentHead

        self.points.append([cx, cy])
        distance = math.hypot(cx-px, cy-py)
        self.lengths.append(distance)
        self.current_length += distance
        self.previous_head = cx, cy 

        cv2.rectangle(imgMain, (self.foodx, self.foody), (self.foodx+40, self.foody+40), (0,255,255), cv2.FILLED)

        
        print("## fingerX, fingerY: " + str(cx) + ", " + str(cy))
        print("## foodx, foody:" + str(self.foodx)+ ", " + str(self.foody))
        print(self.points)


        ##length reduction 
        if self.current_length > self.allowed_length:
            for i, length in enumerate(self.lengths):
                self.current_length -= length 
                self.lengths.pop(i)
                self.points.pop(i)
                if self.current_length < self.allowed_length:
                    break;
            
        #Draw sanke 
        for i, point in enumerate(self.points):
            if i != 0:
                cv2.line(imgMain, self.points[i-1], self.points[i], (0,0,255), 20) 
                
            cv2.circle(imgMain, self.points[-1], 20, (200,0,200), cv2.FILLED)


        #check if the snake eats food 
        if (self.foodx - 20) <  cx < (self.foodx + 45) and (self.foody - 20) < cy < (self.foody + 45):
            self.foodPoint = self.randomizeFood()
            self.score += 1
            self.allowed_length += 30

        
        #display text
        imgMain  = cv2.putText(imgMain, f'SCORE: {self.score}', (10, 690), self.font, 1, (0,255,0), 2, cv2.LINE_AA)

        return imgMain


        


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

    cv2.imshow("Image", img)
    cv2.waitKey(1)