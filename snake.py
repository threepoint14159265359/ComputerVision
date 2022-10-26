import pygame,sys,random
import pygame.gfxdraw
from pygame.math import Vector2
from HandDetector import * 
import time

## some globals
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
game_window_font = pygame.font.SysFont('sans', 15)


class SNAKE:
	def __init__(self):
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(0,0)
		self.new_block = False
		self.pause = False

		self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
		self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
		self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
		self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
		
		self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
		self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
		self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
		self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

		self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
		self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

		self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
		self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
		self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
		self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
		self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

	def draw_snake(self):
		self.update_head_graphics()
		self.update_tail_graphics()

		for index,block in enumerate(self.body):
			x_pos = int(block.x * cell_size)
			y_pos = int(block.y * cell_size)
			block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

			if index == 0:
				screen.blit(self.head,block_rect)
			elif index == len(self.body) - 1:
				screen.blit(self.tail,block_rect)
			else:
				previous_block = self.body[index + 1] - block
				next_block = self.body[index - 1] - block
				if previous_block.x == next_block.x:
					screen.blit(self.body_vertical,block_rect)
				elif previous_block.y == next_block.y:
					screen.blit(self.body_horizontal,block_rect)
				else:
					if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
						screen.blit(self.body_tl,block_rect)
					elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
						screen.blit(self.body_bl,block_rect)
					elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
						screen.blit(self.body_tr,block_rect)
					elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
						screen.blit(self.body_br,block_rect)

	def update_head_graphics(self):
		head_relation = self.body[1] - self.body[0]
		if head_relation == Vector2(1,0): self.head = self.head_left
		elif head_relation == Vector2(-1,0): self.head = self.head_right
		elif head_relation == Vector2(0,1): self.head = self.head_up
		elif head_relation == Vector2(0,-1): self.head = self.head_down

	def update_tail_graphics(self):
		tail_relation = self.body[-2] - self.body[-1]
		if tail_relation == Vector2(1,0): self.tail = self.tail_left
		elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
		elif tail_relation == Vector2(0,1): self.tail = self.tail_up
		elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

	def move_snake(self):
		if not(self.pause):
			if self.new_block == True:
				body_copy = self.body[:]
				body_copy.insert(0,body_copy[0] + self.direction)
				self.body = body_copy[:]
				self.new_block = False
			else:
				body_copy = self.body[:-1]
				body_copy.insert(0,body_copy[0] + self.direction)
				self.body = body_copy[:]

	def pause_snake(self):
		self.pause = True		

	def add_block(self):
		self.new_block = True

	def play_crunch_sound(self):
		self.crunch_sound.play()

	def reset(self):
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(0,0)


class FRUIT:
	def __init__(self):
		self.randomize()

	def draw_fruit(self):
		fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
		screen.blit(apple,fruit_rect)
		#pygame.draw.rect(screen,(126,166,114),fruit_rect)

	def randomize(self):
		self.x = random.randint(0,cell_number - 1)
		self.y = random.randint(0,cell_number - 1)
		self.pos = Vector2(self.x,self.y)


class MAIN:
	def __init__(self):
		self.snake = SNAKE()
		self.fruit = FRUIT()
		self.game_paused = False
		self.snake_speed_illusion = 0

		self.close_window_icon = pygame.image.load('Graphics/close_window_icon.png').convert_alpha()
		# self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
		# self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
		# self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

	def update(self):
		if self.snake_speed_illusion >= 2: 
			self.snake.move_snake()
			self.snake_speed_illusion = 0
		self.check_collision()
		self.check_fail()
		self.check_puased()

	def draw_elements(self):
		self.draw_grass()
		if not(self.game_paused): 
			self.fruit.draw_fruit()
			self.snake.draw_snake()
			self.draw_score()
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
	

	def check_puased(self):
		if self.game_paused: 
			self.snake.pause_snake()
			self.draw_paused_menu()

	def draw_paused_menu(self):
		window_text = "Game Paused"
		text_surface = game_window_font.render(window_text,True,(200,200,200))
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
		# apple image 
		temp_apple = pygame.transform.scale(apple, (1.5 * cell_size, 1.5 * cell_size) )
		# draw the apple
		screen.blit(apple, (12 * int((cell_size/2)), 12 * int((cell_size/2)) ))



		#TODO: so far, we have done---> when we make a fist, and the game is paused, the snake is paused as well
		       ## display some simple rectagle that shows three buttons: continue, Change Speed, Quit 
			   ## the button on clicks would be handled by the game clicker_simulator.py
			   ## display game puased
			   ## display current and high scores
		       ## minimalistic design

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
		apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
		bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)
		pygame.draw.rect(screen,(167,209,61),bg_rect)
		screen.blit(score_surface,score_rect)
		screen.blit(apple,apple_rect)
		pygame.draw.rect(screen,(56,74,12),bg_rect,2)



### CV2 elements
cap = cv2.VideoCapture(0)
cap.set(3, 800)
cap.set(4, 800)

## hand detection 
hand_detector = HandDetector(detectionCon=0.1, maxHands=1)
main_game = MAIN()


while True:

	# fill the screen with green color 
	screen.fill((175,215,70)) 

	# read frames from the camera 
	_, img = cap.read() 
	img.flags.writeable = False 
	# flip the image at each frame
	img = cv2.flip(img,1)
	# detect hands on each frame
	img = hand_detector.find_hands(img, draw = False) 
	# read landmark list
	lmlist, _ = hand_detector.find_landmarks_pos(img, draw=False)	
	
	# read the driection of hand motoin from hand_detector
	direction = hand_detector.get_hand_motion_direction(img)

	# decide snake direction
	if direction == HandDetector.DIRECTION.UP:
		if main_game.snake.direction.y != 1:
			main_game.snake.direction = Vector2(0,-1)
	elif direction == HandDetector.DIRECTION.RIGHT:
		if main_game.snake.direction.x != -1:
			main_game.snake.direction = Vector2(1,0)
	elif direction == HandDetector.DIRECTION.DOWN:
		if main_game.snake.direction.y != -1:
			main_game.snake.direction = Vector2(0,1)	
	elif direction == HandDetector.DIRECTION.LEFT:
		if main_game.snake.direction.x != 1:
			main_game.snake.direction = Vector2(-1,0)
	
	# check pygame events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		# if event.type == SCREEN_UPDATE:
		# 	main_game.update()
	
	# check if the game is puased -- if the index finger is closed, the game is puased
	if len(lmlist) != 0: 
	 	if  not(hand_detector.is_index_finger_open()): 
	 		main_game.game_paused = True
	
	# draw game elements and update the game
	main_game.draw_elements()
	main_game.update()

	# update pygame
	pygame.display.update()
	# set fps
	clock.tick(60)