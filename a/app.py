import pygame
import random
import sys
pygame.init()
pygame.font.init()

#GLOBALS VARS
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

shapes = [S, Z, I, O, J, L, T]
shapes_colors = [green, red, blue, yellow, darkYellow, darkBlue, purple]

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shapes_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_pos = {}): # return two dimension array full of colors
    grid = [[black for _ in range(10)] for _ in range(20)]  # 20 rows 10 cols

    for y in range(len(grid)): # 20
        for x in range(len(grid[y])): # 10
            if (x,y) in locked_pos: # if (x,y) equal a key in locked_pos
                color = locked_pos[(x,y)] # get the value of that key
                grid[y][x] = color
    
    return grid

def convert_shape_format(piece): # return possible positions of the piece -> [(x1, y1), (x2, y2), ...]
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)] # -> sublist

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))
    
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

def valid_space(piece, grid):
    accepted_position = [[(x, y) for x in range(10) if grid[y][x] == black] for y in range(20)]  #grid's color is black -> available
    accepted_position = [i for sublist in accepted_position for i in sublist] #[[(0,1)],[(0,2)]] -> [(0,1),(0,2)]
    
    formatted = convert_shape_format(piece)

    for position in formatted:
        if position not in accepted_position:
            if position[1] > -1: #y start at -1 in order to look like falling down
                return False
    return True

def check_lost(positions):
    for position in positions:
        x, y = position
        if y < 1:
            return True
    return False 

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(surface, text, size, color):
    
    font = pygame.font.SysFont('arial', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - (label.get_height() / 2)))
       
        
        

def draw_grid(surface, grid):
    startX = top_left_x
    startY = top_left_y
    for y in range(len(grid)):
        pygame.draw.line(surface, gray, (startX, startY + y *  block_size), (startX + play_width, startY + y * block_size))
        for x in range(len(grid[y])): 
            pygame.draw.line(surface, gray, (startX + x * block_size, startY), (startX + x * block_size, startY + play_height))
        
    
def clear_rows(grid, locked_position):
    fullRowCount = 0
    for y in range(len(grid) -1, -1, -1):
        row = grid[y]
        if black not in row: # row is full
            fullRowCount += 1
            index = y
            for x in range(len(row)):
                try:
                    del locked_position[(x,y)]
                except:
                    continue
    
    if fullRowCount > 0:
        for key in sorted(list(locked_position), key = lambda x: x[1], reverse=True):
            x, y = key
            if y < index: # y value is above the row that's full
                newKey = (x, y + fullRowCount) # shift rows above
                locked_position[newKey] = locked_position.pop(key)
    return fullRowCount

def last_score():
    with open("d:/Users/Public/Documents/python/Tetris/score.txt", 'r', encoding='utf8') as f:
        lines = f.readline().split()
        last_score = int(lines[0])
        # player = lines[1]
        
    return last_score

def update_score(newScore = 0):
    # lastScore = last_score()
    # with open("d:/Users/Public/Documents/python/Tetris/score.txt", 'r') as f:
    #     lines = f.readlines()
    #     last_score = lines[0].strip()

    with open("d:/Users/Public/Documents/python/Tetris/score.txt", 'w') as f:
        # if (int(lastScore) != newScore):
        #     f.write(str(newScore))
        # else:
        #     f.write(str(lastScore))
        f.write((str(newScore)))

def high_score():

    with open("d:/Users/Public/Documents/python/Tetris/highscore.txt", 'r') as f:
        lines = f.readlines()
        high_score = lines[0].strip()
    return high_score 
def update_high_score(lastScore):
    highScore = high_score()
    with open("d:/Users/Public/Documents/python/Tetris/highscore.txt", 'w') as f:
        if (int(highScore) > int(lastScore)):
            f.write(str(highScore))
        else:
            f.write(str(lastScore))
def draw_next_shapes(piece, surface):
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Next Shape', 1, white)

    startX = top_left_x + play_width + 50
    startY = top_left_y + play_height / 2 - 100 
    format = piece.shape[piece.rotation % len(piece.shape)] # -> sublist 

    for y, line in enumerate(format):
        row = list(line)
        for x, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, piece.color, (startX +  x * block_size, startY + y * block_size + 10, block_size, block_size), 0)

    surface.blit(label, (startX + 10, startY  - 30))

def draw_window(surface, grid,user_text, score = 0, last_score = 0 , high_score = 0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Tetris', 1, (255,255,255))
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30)) #middle of the screen (label,x,y)

    #Current_score
    label = font.render('Score' + ":  " + str(score), 1, white)

    startX = top_left_x + play_width + 50
    startY = top_left_y + play_height / 2 - 100 
     
    surface.blit(label, (startX + 10, startY  + 160))

    #Last_score
    label = font.render('Last Score' + ":  " + str(last_score), 1, white)

    startX = top_left_x - 200
    startY = top_left_y + play_height / 2 - 100 
    surface.blit(label, (startX + 10, startY  + 160))
    # Player name:
    label = font.render('Player' + ":  " + user_text, 1, white)

    startX = top_left_x - 200
    startY = top_left_y + play_height / 2 - 100 
    surface.blit(label, (startX + 10, startY  + 100))
    # High score
    label = font.render('High Score' + ":  " + str(high_score), 1, white)

    startX = top_left_x - 200
    startY = top_left_y + play_height / 2 - 400
    surface.blit(label, (startX + 10, startY  + 160))

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (top_left_x + x * block_size, top_left_y + y * block_size, block_size, block_size), 0)
    pygame.draw.rect(surface, red, (top_left_x, top_left_y,play_width,play_height), 4)

    draw_grid(surface, grid)
    #pygame.display.update()

def main(window, user_text):
    lastScore = last_score()
    locked_position = {}
    grid = create_grid(locked_position)
    change_piece = False
    run  = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0  
    level_time = 0
    fall_speed = 0.27
    score = 0
    highScore = high_score()
    while run:
        grid = create_grid(locked_position)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.01

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
        
        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x,y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece: # before change piece need to reset locked positions by give them color
            for pos in shape_pos: # locked_position = {(1, 2): black, (2, 3): black, (3, 4): black, ...}
                locked_position[pos] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            value = clear_rows(grid,locked_position)
            if value == 2:
                score += value * 20
            elif value == 0:
                continue
            else:
                score += value * 10
            
            #score += clear_rows(grid,locked_position) * 10


        draw_window(window, grid, user_text, score, lastScore, highScore)
        draw_next_shapes(next_piece, window)
        pygame.display.update()

        if check_lost(locked_position):
            draw_text_middle(window, 'You Lost!', 80, white)
            pygame.display.update()
            pygame.time.delay(1500)
            update_score(score)
            update_high_score(score)
            run = False
            # update_score(score)
    
    

def main_menu(window):
    
    input_rect = pygame.Rect(top_left_x + play_width / 2-120, top_left_y + play_height / 2 + 45, 180, 60)
    clock = pygame.time.Clock()
    color_active = pygame.Color(red)
    color_passive = pygame.Color(purple)
    color_text_box = color_passive
    active = False
    user_text = ''
    font = pygame.font.SysFont('arial', 60, bold=True)
    label = font.render('Type name:', 1, white)
    text_surface = font.render(user_text, True, blue)
    # run = True
    
    while True:
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
        # Unicode standard is used for string
        # formation
                
                else:
                    user_text += event.unicode
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    user_text = user_text[:-1]
                    main(window,user_text)
        window.fill(black)
        if active:
            color_text_box = color_active
        else:
            color_text_box = color_passive
            

        pygame.draw.rect(window, color_text_box, input_rect)
        text_surface = font.render(user_text, True, (255, 255, 255))
        window.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - (label.get_height() / 2)))
        window.blit(text_surface, (input_rect.x+5, input_rect.y))
        input_rect.w = max(100, text_surface.get_width()+10)
        pygame.display.flip()
        clock.tick(60)
                
    

window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')
main_menu(window)
