from blinker import NamedSignal
import pygame as pg
from CONSTS import *
import math
import random as ran
import time



class Game: 
    def __init__(self, window) -> None:
        self.window = window
        self.score = 0
        self.hight_score = 0
        self.food_img = pg.transform.scale(pg.image.load(FOOD_URL).convert_alpha(), \
        (FOOD_IMG_WIDTH, FOOD_IMG_HEIGHT)) 
        self.food_rect = self.food_img.get_rect() ## will be used to determine collisions
        self.food_x, self.food_y = self.__randomize_food()
        self.snake = [[]] 
        self.__init_snake()
        self.direction = INIT_SNAKE_DIRECTION

    def set_direction(self, direc):
        self.direction = direc

    def set_scene(self):
        # Fill the background
        self.window.fill((0,200,0))
        # draw walls
        self.playground = pg.draw.rect(self.window, WALL_COLOR, \
            [WALL_TOPLEFT_X, WALL_TOPLEFT_Y, WALL_WIDHT, WALL_HEIGHT], \
            WALL_THICKNESS);        
        # draw score
        font = pg.font.Font(FONT_URL, FONT_SIZE)
        rendered_score = font.render(f'Your Score: {str(self.score)}'  , True, FONT_COLOR)
        self.window.blit(rendered_score, (SCORE_X,SCORE_Y))
        # draw high score
        rendered_high_score = font.render(f'High Score: {str(self.score)}'  , True, FONT_COLOR)
        self.window.blit(rendered_high_score, (HIGH_SCORE_X, HIGH_SCORE_Y))
        #draw food
        self.window.blit(self.food_img, (self.food_x, self.food_y))
        #draw snake
        self.__draw_snake()
        print(f'SNAKE: {self.snake[0]} , FOOD {[[self.food_x, self.food_y]]}') 


    def __randomize_food(self):
        food_x, food_y = ran.randint(100, abs(WIDTH - 200)), ran.randint(100,abs(HEIGHT - 300))
        ## NOTE: check if the snake point lies on the snake's body --- recursively call the same function to generater new points
        return food_x, food_y

    def __init_snake(self): 
        self.snake = [[SNAKE_START_X, SNAKE_START_Y]]
        self.snake.append([SNAKE_START_X - SNAKE_BLOCK_SIZE, SNAKE_START_Y]) 
        self.snake.append([SNAKE_START_X - 2*SNAKE_BLOCK_SIZE, SNAKE_START_Y])
        self.snake.append([SNAKE_START_X - 3*SNAKE_BLOCK_SIZE, SNAKE_START_Y])
    
    def __draw_snake(self):
        head = True
        for block in self.snake:
            if head: 
                pg.draw.rect(self.window, SNAKE_HEAD, (block[0], block[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))
                # draw eyes with the body color
                pg.draw.rect(self.window, SNAKE_BODY, (block[0] + 5, block[1] + 15, SNAKE_EYE_SIZE, SNAKE_EYE_SIZE))
                pg.draw.rect(self.window, SNAKE_BODY, (block[0] + 20, block[1] + 15, SNAKE_EYE_SIZE, SNAKE_EYE_SIZE))
                head = False
            else: 
                pg.draw.rect(self.window, SNAKE_BODY, (block[0], block[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))

    def move(self):
        self.snake = self.snake[-1:] + self.snake[:-1]
        if self.direction == 1: 
            self.snake[0][0] = self.snake[1][0]
            self.snake[0][1] = self.snake[1][1] - SNAKE_BLOCK_SIZE
        if self.direction == 3: 
            self.snake[0][0] = self.snake[1][0]
            self.snake[0][1] = self.snake[1][1] + SNAKE_BLOCK_SIZE
        if self.direction == 2: 
            self.snake[0][1] = self.snake[1][1]
            self.snake[0][0] = self.snake[1][0] + SNAKE_BLOCK_SIZE
        if self.direction == 4 : 
            self.snake[0][1] = self.snake[1][1]
            self.snake[0][0] = self.snake[1][0] - SNAKE_BLOCK_SIZE