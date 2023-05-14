import pygame
from GlobalVar import *
def create_grid(locked_pos = {}): # return two dimension array full of colors
    grid = [[black_image for _ in range(10)] for _ in range(20)]  # 20 rows 10 cols

    for y in range(len(grid)): # loop row
        for x in range(len(grid[y])): # loop column in the row
            if (x,y) in locked_pos: # check if the position (x,y) is in the locked_pos dictionary
                # if it is, color the square at that position with the color specified in the dictionary
                grid[y][x] = locked_pos[(x,y)] 
    # return the resulting grid
    return grid

def draw_grid(surface, grid):# draw horizontal and vertical lines
    startX = top_left_x
    startY = top_left_y
    for y in range(len(grid)):
        pygame.draw.line(surface, gray, (startX, startY + y *  block_size), (startX + play_width, startY + y * block_size))
        for x in range(len(grid[y])): 
            pygame.draw.line(surface, gray, (startX + x * block_size, startY), (startX + x * block_size, startY + play_height))