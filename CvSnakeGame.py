
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