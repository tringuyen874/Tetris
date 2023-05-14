import random
from GlobalVar import *
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shapes_colors[shapes.index(shape)]
        self.rotation = 0

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def convert_shape_format(piece): # return possible positions of the piece -> [(x1, y1), (x2, y2), ...]
    positions = []
    # get the sublist of the shape attribute of the piece object that corresponds to the current rotation
    format = piece.shape[piece.rotation % len(piece.shape)] # -> sublist

    # iterate through each string in the format list
    for i, line in enumerate(format):
        row = list(line)
        # iterate through each character in the string
        for j, column in enumerate(row):
            # if the character is a '0', add the position of that character to the positions list as a tuple
            if column == '0':
                positions.append((piece.x + j, piece.y + i))
    
    # adjust the positions of the piece by subtracting 2 from the x value of each position and subtracting 4 from the y value
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

def draw_next_shapes(piece, surface):
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Next Shape', 1, white)
    startX = top_left_x + play_width + 50
    startY = top_left_y + play_height / 2 - 100 
    next_shape_area = pygame.Rect(startX,startY- 30,150,label.get_height() + 10 + block_size *5)
    shape_format = piece.shape[piece.rotation % len(piece.shape)] # -> sublist 
    surface.fill(gray, next_shape_area)
    for y, line in enumerate(shape_format):
        row = list(line)
        for x, column in enumerate(row):
            if column == '0':
                surface.blit(piece.color, (startX +  x * block_size, startY + y * block_size + 10))
    
    surface.blit(label, (startX + 10, startY  - 30))

def clear_rows(grid, locked_position): 
    List = []  
    fullRowCount = 0
    clear_sound.set_volume(1)
    for y in range(len(grid) -1, -1, -1):
        row = grid[y]
        
        if black_image not in row: # row is full
            fullRowCount += 1
            index = y
            for x in range(len(row)):
                try:
                    del locked_position[(x,y)]
                except:
                    continue
            sound.stop()
            clear_sound.play()    
            List.append(index)
                   
    if fullRowCount > 0: 
        for key in sorted(list(locked_position), key = lambda x: x[1], reverse=True):
            x, y = key
                # y value is above the row that's full
            if len(List) == 0:
                continue 
            if len(List) == 1:
                if y > List[0]:
                    continue
                if y < List[0]:
                    newKey = (x, y + 1) # shift rows above
                    locked_position[newKey] = locked_position.pop(key)
            if len(List) == 2:
                if y > List[0]:
                    continue
                if List[1] < y < List[0]:
                    newKey = (x, y + 1) # shift rows above
                    locked_position[newKey] = locked_position.pop(key)
                if y < List[1]:
                    newKey = (x, y + 2) # shift rows above
                    locked_position[newKey] = locked_position.pop(key)
            if len(List) == 3:
                if y > List[0]:
                    continue
                if  List[1] < y < List[0]:
                    newKey = (x, y + 1) # shift rows above
                    locked_position[newKey] = locked_position.pop(key)
                if List[2] < y < List[1]:
                    newKey = (x, y + 2) # shift rows above
                    locked_position[newKey] = locked_position.pop(key)     
                if y < List[2]:
                    newKey = (x,y + 3)
                    locked_position[newKey] = locked_position.pop(key)
            if len(List) == 4:
                if y > List[0]:
                    continue
                if List[1] < y < List[0]:
                    newKey = (x, y + 1) # shift rows above
                    locked_position[newKey] = locked_position.pop(key)
                if List[2] < y < List[1]:
                    newKey = (x, y + 2) # shift rows above
                    locked_position[newKey] = locked_position.pop(key)     
                if List[3] < y < List[2]:
                    newKey = (x,y + 3)
                    locked_position[newKey] = locked_position.pop(key)
                if y < List[3]:
                    newKey = (x,y + 4)
                    locked_position[newKey] = locked_position.pop(key)
    
    return fullRowCount

def valid_space(piece, grid):
    # generate a list of tuples representing the positions on the grid that are currently occupied by the color black
    accepted_position = [[(x, y) for x in range(10) if grid[y][x] == black_image] for y in range(20)]  
    # flatten the list of lists into a single list
    accepted_position = [i for sublist in accepted_position for i in sublist] 
    
    # get a list of tuples representing the positions that the piece occupies in its current rotation
    occupied_positions = convert_shape_format(piece)

    for position in occupied_positions:
        # if the position is not in the accepted_position list, return False
        if position not in accepted_position:
            if position[1] > -1: # prevent the piece from occupying positions above the top of the grid
                return False
    # if all of the positions in the occupied_positions list are in the accepted_position list, return True
    return True

def check_lost(positions):
    for position in positions:
        x, y = position
        if y < 1:
            # If the y value is less than 1, the current piece has reached the top of the grid and the player has lost the game
            return True
    return False 