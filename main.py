from Init import *
import pygame
import pygame.gfxdraw
from HandDetector import * 
import sys
from pygame.math import Vector2
from Snake import *
from Fruit import *
from Game import *
import autopy
import numpy as np



#################################
## CV elements
wCam, hCam = 720,576 # 720, 570 with thirty fps is amazing
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
cap.set(cv2.CAP_PROP_EXPOSURE, 0.1)
################################


hand_detector = HandDetector(detectionCon=0.1, maxHands=1)
main_game = SnakeGame()

def handle_direction(direction):
    if direction == HandDetector.DIRECTION.UP and main_game.snake.direction.y != 1:
        main_game.snake.direction = Vector2(0,-1)
    elif direction == HandDetector.DIRECTION.RIGHT and main_game.snake.direction.x != -1:
        main_game.snake.direction = Vector2(1,0)
    elif direction == HandDetector.DIRECTION.DOWN and main_game.snake.direction.y != -1:
        main_game.snake.direction = Vector2(0,1)	
    elif direction == HandDetector.DIRECTION.LEFT and main_game.snake.direction.x != 1:
        main_game.snake.direction = Vector2(-1,0)

def handle_paused_menu(mouse_coords):
    play_x, play_y, play_w, play_h = 310, 544, 173, 38 
    play_rect = pygame.rect.Rect(play_x, play_y, play_w, play_h)
    quit_x, quit_y, quit_w, quit_h = 496, 544, 42, 38 
    quit2_x, quit2_y, quit2_w, quit2_h = 596, 188, 16, 16 
    quit_rect = pygame.rect.Rect(quit_x, quit_y, quit_w, quit_h)
    quit2_rect = pygame.rect.Rect(quit2_x, quit2_y, quit2_w, quit2_h) 
    home_x, home_y, home_w, home_h = 256, 544, 42, 38
    home_rect = pygame.rect.Rect(home_x, home_y, home_w, home_h)
    if play_rect.collidepoint(mouse_coords):
        main_game.game_paused = False
    elif quit_rect.collidepoint(mouse_coords) or quit2_rect.collidepoint(mouse_coords):
        close = input("Are you sure, you wanna quit the game?[y/n] : ")
        if close == 'y':
            pygame.quit()
            sys.exit()
    elif home_rect.collidepoint(mouse_coords):
        print("HOME MENU DISPLAY")


def main(): 
    ##################################
    ## mouse related constants
    frame_reduction = 100
    smoothening = 12
    pTime = 0
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0
    mouse_screen_width, mouse_screen_height = autopy.screen.size()
    mouse_mode = False
    
    #################################
    while True:
        screen.fill((175,215,70))
        _, img = cap.read()
        if not(mouse_mode):
            img = cv2.flip(img, 1)
        img = hand_detector.find_hands(img, draw = False) 
        lmlist, _ = hand_detector.find_landmarks_pos(img, draw=False)    
        direction= hand_detector.get_hand_motion_direction(img)
        handle_direction(direction=direction)


        # only if the little finger is open - the game would be paused
        if len(lmlist) != 0 and not(hand_detector.is_index_finger_open()) \
                            and hand_detector.is_little_finger_open()\
                            and not(hand_detector.is_middle_finger_open())\
                            and not(hand_detector.is_ring_finger_open()):
            main_game.game_paused = True
            mouse_mode = True
        
        # if the game is not in play mode, the mouse is able to move
        if not(main_game.game_paused):
            mouse_mode = False # we don't want the mouse in the play mode

        # mouse curser handeling
        if len(lmlist) != 0 and mouse_mode:
            index_x, index_y = hand_detector.get_index_finger_landmark()
            ## movements mode 
            if hand_detector.is_index_finger_open() \
                and not(hand_detector.is_little_finger_open())\
                and not(hand_detector.is_middle_finger_open())\
                and not(hand_detector.is_ring_finger_open()): 
                x3 = np.interp(index_x, (frame_reduction, wCam - frame_reduction), (0, mouse_screen_width))
                y3 = np.interp(index_y, (frame_reduction, hCam - frame_reduction), (0, mouse_screen_height))
                ## somethen the values for the mous curser to move to
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                ## move mouse 
                autopy.mouse.move(mouse_screen_width - clocX, clocY)
                plocX, plocY = clocX, clocY
            
            # ## click mode - on fist
            if hand_detector.is_hand_complete_fist():  
                #distance, _, _  = hand_detector.find_distance_between_landmarks(12, 8, img, draw=False)
                #print(distance)
                #if distance < 20: # In other words if the are almost touching each other
                print("Clicked");
                autopy.mouse.click(delay=0.2); 

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and main_game.game_paused:
                mouse_coords = pygame.mouse.get_pos()
                handle_paused_menu(mouse_coords=mouse_coords)
                
                
        

        main_game.draw_elements()
        main_game.update()
        
        
        pygame.display.update()
        clock.tick(30)



main()