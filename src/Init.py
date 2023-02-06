import pygame

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
apple1 =  pygame.transform.scale(pygame.image.load('Graphics/apple.png').convert_alpha() , (40, 40)) 
apple2 =  pygame.transform.scale(pygame.image.load('Graphics/apple1.png').convert_alpha() , (60, 60))
trophy1 = pygame.transform.scale(pygame.image.load('Graphics/trophy.png').convert_alpha() , (35, 32))
trophy2 = pygame.transform.scale(pygame.image.load('Graphics/trophy.png').convert_alpha() , (60, 60))  
home_icon = pygame.transform.scale(pygame.image.load('Graphics/home_icon.png').convert_alpha(), (55, 55))
quit_icon = pygame.transform.scale(pygame.image.load('Graphics/quit_icon.png').convert_alpha(), (45, 45))
game_font =  pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
game_font1 =  pygame.font.Font('Font/PoetsenOne-Regular.ttf', 40)
game_window_font = pygame.font.SysFont('sans', 15)