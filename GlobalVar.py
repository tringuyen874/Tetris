import pygame
screen_width = 800
screen_height = 700
play_width = 300
play_height = 600
block_size = 30 

top_left_x = (screen_width - play_width) // 2 #250
top_left_y = (screen_height - play_height) #100

green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 255, 255)
yellow = (255, 255, 0)
darkYellow = (255, 165, 0)
darkBlue = (0, 0, 255)
purple = (128, 0, 128)
black = (0, 0, 0)
gray = (128, 128, 128)
white = (255, 255, 255)

black_image = pygame.image.load(f"Tetris/images/Black.png")
background_image = pygame.image.load(f"Tetris/images/bg.png")
background_image = pygame.transform.scale(background_image, (screen_width,screen_height))
title = pygame.image.load(f"Tetris/images/title.png")
title = pygame.transform.scale(title, (150,50))
open_title = pygame.image.load(f"Tetris/images/open_title.png")
open_title = pygame.transform.scale(open_title, (600,150))
setting = pygame.image.load(f"Tetris/images/setting.png")
plus = pygame.image.load(f"Tetris/images/plus.png")
plus = pygame.transform.scale(plus, (30,30))
minus = pygame.image.load(f"Tetris/images/minus.png")
minus = pygame.transform.scale(minus, (30,30))
replay = pygame.image.load(f"Tetris/images/replay.png")
replay = pygame.transform.scale(replay, (30,30))
new_level = 0.005
new_volume = 0.5
#setting = pygame.transform.scale(setting, (60,60))
# Initialize the mixer module
pygame.mixer.init()
moniter = {'top': 0, 'left':283, 'width':800, 'height':750}
# Load the sound file
sound = pygame.mixer.Sound('Tetris/sound/play_sound.mp3')
#sound.set_volume = (0.5)
clear_sound = pygame.mixer.Sound('Tetris/sound/ClearSound.mp3')
# clear_sound_volume = clear_sound.get_volume()

# Play the sound
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

B = [['.....',
      '.....',
      '..0..',
      '.....',
      '.....']]
shapes = [S, Z, I, O, J, L, T, B]
shape_string = ["S", "Z", "I", "O", "J", "L", "T", "B"]
shapes_colors = []
for i in shape_string:
    image = pygame.image.load(f"Tetris/images/{i}.png")
    new_image = pygame.transform.scale(image, (30,30))
    shapes_colors.append(new_image)
# shapes_colors = [green, red, blue, yellow, darkYellow, darkBlue, purple]