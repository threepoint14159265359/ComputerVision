from Init import *
import pygame
from HandDetector import * 
from Snake import *
from Fruit import *


class SnakeGame:
	def __init__(self):
		self.snake = SNAKE()
		self.fruit = FRUIT()
		self.game_paused = False
		self.snake_speed_illusion = 0
		self.high_score = 0
		self.close_window_icon = pygame.image.load('Graphics/close_window_icon.png').convert_alpha()
		self.load_time = False

	def set_load_time(self, time):
		self.load_time = time

	def update(self):
		if not(self.game_paused) and self.snake_speed_illusion >= 3: 
			self.snake.move_snake()
			self.snake_speed_illusion = 0
		self.check_collision()
		self.check_fail()
		self.check_pause()
		self.update_highscore()

	def update_highscore(self):
		cscore = len(self.snake.body) - 3
		if self.high_score <= cscore:
			self.high_score = cscore

	def draw_elements(self):
		self.draw_grass()
		if not(self.game_paused): 
			self.fruit.draw_fruit()
			self.snake.draw_snake()
			self.draw_score()
			self.draw_highscore()
		self.snake_speed_illusion += 1
		

	def check_collision(self):
		if self.fruit.pos == self.snake.body[0]:
			self.fruit.randomize()
			self.snake.add_block()
			self.snake.play_crunch_sound()

		for block in self.snake.body[1:]:
			if block == self.fruit.pos:
				self.fruit.randomize()

	def check_fail(self):
		if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
			self.game_over()

		for block in self.snake.body[1:]:
			if block == self.snake.body[0]:
				self.game_over()
		
	def game_over(self):
		self.snake.reset()
	
	def check_pause(self):
		if self.game_paused: 
			self.draw_paused_menu()
		

	def draw_paused_menu(self):
		window_text = "Game Paused"
		text_surface = game_window_font.render(window_text,True,(200,200,200))
		x, y = 9 * int((cell_size/2)), 9 * int((cell_size/2))
		w, h = 11 * cell_size, 11 * cell_size
		background_rect = pygame.Rect(9 * int((cell_size/2)), 9 * int((cell_size)/2), 11 * cell_size, 11 * cell_size)
		# draw greenish background for the window
		pygame.draw.rect(screen, (155,209,61), background_rect) 
		# draw black border for the window 
		pygame.draw.rect(screen, (56,74,12), background_rect, width = 1, \
						border_top_left_radius=10, border_top_right_radius=10) 
		# draw black top panel for the window
		pygame.draw.rect(screen, (56,74,12), (9 * int((cell_size/2)),  
						9 *	int((cell_size/2)), 11 * cell_size, 28), \
						border_top_left_radius=10, border_top_right_radius=10)
		# draw the window_close icon on the top right corner of the panel
		screen.blit(self.close_window_icon, (29.5 * int(cell_size/2) + 2, 9 * int(cell_size/2) + 3))
		# draw the 'game paused' text on the top left of the panel
		screen.blit(text_surface, (9 * int((cell_size/2)) + 7, 9 * int((cell_size)/2) + 8))
		# draw the score and high score on the window
		score_text = str(len(self.snake.body) - 3)
		highscore_text = str(self.high_score)
		score_surface1 = game_font1.render(score_text,True,(56,74,12))
		score_surface2 = game_font1.render(highscore_text,True,(56,74,12))
		# draw apple
		screen.blit(apple2, (x + cell_size, y + int(h/4)))
		# draw score
		screen.blit(score_surface1, (x + 3 * cell_size, y  + int(h/4) + 10 ))
		# draw trophy 
		screen.blit(trophy2, ((x + int(w/2) + cell_size), (y + int(h/4))))
		# draw high score
		screen.blit(score_surface2, ((x + int(w/2) + 3 * cell_size), y + int(h/4) + 10))
		# draw buttons
		# draw play button
		play_rect = pygame.rect.Rect(x + int(w/3) - 18 , (y + h) - 2 * cell_size, int(w/3) + 30 , (2 * cell_size) - 35)
		pygame.draw.rect(screen,(0,128,255), play_rect, border_radius=15)
		play = "Play"
		text_rend_rect = game_font.render(play,True, "white")
		screen.blit(text_rend_rect, ((play_rect.centerx - 25), (play_rect.centery - 15)))
		# draw home button
		screen.blit(home_icon, (x + int(w/3) - 4* cell_number, (y + h) - int(2.12 * cell_size)))
		# draw quit button
		screen.blit(quit_icon, ((x + (w - int(w/3)) + cell_number), (y + h) - int(2 * cell_size)) )
		
	def draw_grass(self):
		grass_color = (167,209,61)
		for row in range(cell_number):
			if row % 2 == 0: 
				for col in range(cell_number):
					if col % 2 == 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)
			else:
				for col in range(cell_number):
					if col % 2 != 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)			

	def draw_score(self):
		score_text = str(len(self.snake.body) - 3)
		score_surface = game_font.render(score_text,True,(56,74,12))
		score_x = int(cell_size * cell_number - 60)
		score_y = int(cell_size * cell_number - 40)
		score_rect = score_surface.get_rect(center = (score_x,score_y))
		apple_rect = apple1.get_rect(midright = (score_rect.left,score_rect.centery))
		bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)
		pygame.draw.rect(screen,(167,209,61),bg_rect)
		screen.blit(score_surface,score_rect)
		screen.blit(apple1,apple_rect)
		pygame.draw.rect(screen,(56,74,12),bg_rect,2)

	def draw_highscore(self):
		highscore_text = str(self.high_score)
		score_surface = game_font.render(highscore_text,True,(56,74,12))
		x, y = int((cell_size*cell_number) - ((3 * cell_size))), 20
		bg_rect = pygame.rect.Rect(x, y, 2 * cell_size, int( 1.05 * cell_size))
		pygame.draw.rect(screen,(167,209,61), bg_rect)
		pygame.draw.rect(screen, (56,74,12), bg_rect, 2) # border
		screen.blit(trophy1, (x+5, y+5))
		screen.blit(score_surface, (x + int(1.2 * cell_size) , y+7))



