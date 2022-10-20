import pygame as pg
from CONSTS import *
import math
import random as ran
import time
import pygame_menu 



def gameover():
    pass

def game_over_menu(window, score):
    menu = pygame_menu.Menu("Game Paused", MENU_WIDHT, MENU_HEIGHT,\
        theme=pygame_menu.themes.THEME_BLUE)
    menu.add.text_input(f' Current Score: {score} ')
    menu.add.button('Resume',gameover )
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(window)
    return menu


class Snake: 
    def __init__(self, window) -> None:
        self.window = window
        self.__direction = 2 # by default, the snake moves towards right
        self.__init_snake()
        self.timer = 0
        
    def __init_snake(self): 
        self.__snake_list = [[int(WIDTH/2), int(HEIGHT/2)]]
        self.__snake_list.append([int(WIDTH/2) - 1 *  SNAKE_BLOCK_SIZE , int(HEIGHT/2)])
        self.__snake_list.append([int(WIDTH/2) - 2 *  SNAKE_BLOCK_SIZE , int(HEIGHT/2)])
        self.__snake_list.append([int(WIDTH/2) - 3 *  SNAKE_BLOCK_SIZE , int(HEIGHT/2)])

    def get_diection(self):
        return self.__direction

    def set_direction(self, direct): 
        self.__direction = direct

    def draw(self): 
        self.timer += 1
        head = True
        for list_of_rects in self.__snake_list: 
            if head:
                head = False
                pg.draw.rect(self.window, SNAKE_HEAD, (list_of_rects[0], list_of_rects[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))
                pg.draw.rect(self.window, SNAKE_BODY, (list_of_rects[0] + 4, list_of_rects[1] + 10, SNAKE_EYE_SIZE , SNAKE_EYE_SIZE))
                pg.draw.rect(self.window, SNAKE_BODY, (list_of_rects[0] + 15, list_of_rects[1] + 10, SNAKE_EYE_SIZE , SNAKE_EYE_SIZE))               
            else: 
                pg.draw.rect(self.window, SNAKE_BODY, (list_of_rects[0], list_of_rects[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))
            
    def move(self):
        if self.timer > 5: 
            self.timer = 0
            self.__snake_list = self.__snake_list[-1:] + self.__snake_list[:-1]
            if self.__direction == 1: 
                self.__snake_list[0][0] = self.__snake_list[1][0]
                self.__snake_list[0][1] = self.__snake_list[1][1] - SNAKE_BLOCK_SIZE
            if self.__direction == 3: 
                self.__snake_list[0][0] = self.__snake_list[1][0]
                self.__snake_list[0][1] = self.__snake_list[1][1] + SNAKE_BLOCK_SIZE
            if self.__direction == 2: 
                self.__snake_list[0][1] = self.__snake_list[1][1]
                self.__snake_list[0][0] = self.__snake_list[1][0] + SNAKE_BLOCK_SIZE
            if self.__direction == 4 : 
                self.__snake_list[0][1] = self.__snake_list[1][1]
                self.__snake_list[0][0] = self.__snake_list[1][0] - SNAKE_BLOCK_SIZE

    def collide(self, x, y, name):
        food_rect = pg.rect.Rect(x, y, FOOD_IMG_WIDTH, FOOD_IMG_HEIGHT)
        for block in self.__snake_list:
            snake_rect = pg.rect.Rect(block[0], block[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE)
            if name == "food" and food_rect.colliderect(snake_rect):
                return True
            elif name == "wall": 
                if self.__direction == 1 and self.__snake_list[0][1] < WALL_THICKNESS: 
                    return True
                elif self.__direction == 3 and self.__snake_list[0][1] > (HEIGHT - WALL_THICKNESS) - SNAKE_BLOCK_SIZE: 
                    return True
                elif self.__direction == 2 and self.__snake_list[0][0] > (WALL_THICKNESS + WIDTH) - 5 * SNAKE_BLOCK_SIZE: 
                    return True
                elif self.__direction == 4 and self.__snake_list[0][0] < WALL_THICKNESS: 
                    return True
        return False

    def update(self): ## note: fix me -- i am giving out some bad behaviour 
        if self.__direction == 1:
            self.__snake_list.append([self.__snake_list[-1][0],  self.__snake_list[-1][1] + SNAKE_BLOCK_SIZE])
        elif self.__direction == 3:
            self.__snake_list.append([self.__snake_list[-1][0],  self.__snake_list[-1][1] - SNAKE_BLOCK_SIZE])
        elif self.__direction == 2:
            self.__snake_list.append([self.__snake_list[-1][0] - SNAKE_BLOCK_SIZE,  self.__snake_list[-1][1]])
        elif self.__direction == 4:
            self.__snake_list.append([self.__snake_list[-1][0] + SNAKE_BLOCK_SIZE,  self.__snake_list[-1][1]])
                

class Game: 
    def __init__(self, window) -> None:
        self.window = window
        self.score = 0
        self.hight_score = 0
        self.food_img = pg.transform.scale(pg.image.load(FOOD_URL).convert_alpha(), \
        (FOOD_IMG_WIDTH, FOOD_IMG_HEIGHT)) 
        self.food_rect = self.food_img.get_rect() ## will be used to determine collisions
        self.font = pg.font.Font(FONT_URL, FONT_SIZE)
        self.food_x, self.food_y = self.__randomize_food()
        self.__snake = Snake(self.window) 
        self.__game_over = False
        
        
    def set_snake_driction(self, direction):
        self.__snake.set_direction(direct=direction)

    def get_snake_direction(self):
        return self.__snake.get_diection()

    def __randomize_food(self):
        food_x, food_y = ran.randint(100, abs(WIDTH - 200)), ran.randint(100,abs(HEIGHT - 300))
        return food_x, food_y


    def __set_game_scene(self):
        self.rendered_score = self.font.render(f'Your Score: {str(self.score)}'  , True, FONT_COLOR)
        self.rendered_high_score = self.font.render(f'High Score: {str(self.hight_score)}'  , True, FONT_COLOR)
        self.window.fill((0,200,0))
        # draw walls
        self.playground = pg.draw.rect(self.window, WALL_COLOR, \
            [WALL_TOPLEFT_X, WALL_TOPLEFT_Y, WALL_WIDHT, WALL_HEIGHT], \
            2 * SNAKE_BLOCK_SIZE);        
        # draw score
        self.window.blit(self.rendered_score, (SCORE_X,SCORE_Y))
        # draw high score
        self.window.blit(self.rendered_high_score, (HIGH_SCORE_X, HIGH_SCORE_Y))
        #draw food
        self.window.blit(self.food_img, (self.food_x, self.food_y))
        #draw snake
        self.__snake.draw()
        
   
    def run(self):
        ## set the scene
        if not (self.__game_over):
            self.__set_game_scene()
            ## move snake
            self.__snake.move()
            ## check for collision against food
            if self.__snake.collide(self.food_x, self.food_y, "food"):
                self.food_x, self.food_y = self.__randomize_food()
                self.score += 1
                self.__snake.update()
            ## check for collision against wall
            if (self.__snake.collide(0, 0, "wall")):
                self.__game_over = True
        else: # GAEM OVE BRANCH  
            game_over_menu(self.window, self.score)
            # resest the score
            self.score = 0
            