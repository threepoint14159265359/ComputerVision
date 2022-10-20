from Snake import *
import pygame
import cv2
from CONSTS import *
import numpy as np


# Initialize
pygame.init()

# Create Window/Display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Initialize Clock for FPS
clock = pygame.time.Clock()

# Intitalize Snake 
game = Game(window)


# Main loop
start = True
while start:
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game.get_snake_direction() != 3: 
                game.set_snake_driction(1)
            elif event.key == pygame.K_DOWN and game.get_snake_direction() != 1:
                game.set_snake_driction(3)
            elif event.key == pygame.K_LEFT and game.get_snake_direction()!= 2:
                game.set_snake_driction(4)
            elif event.key == pygame.K_RIGHT and game.get_snake_direction()!= 4:
                game.set_snake_driction(2)

    # Apply Logic
    """  two threads
        /           \
      /              \
    game-thread  capture-gestures-thread
                            |
                --functionalities capture-gestures-thread icludes:
                    -  direction detection 
                    -  pause-game, play-game mode-detection 
                    -  virtual ai simulation
    """         
    
    game.run()


    
    # Update Display
    pygame.display.update()
    # Set FPS
    clock.tick(FPS)


