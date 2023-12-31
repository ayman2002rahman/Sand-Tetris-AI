import pygame
from enum import IntEnum, auto
import random
import numpy as np

CELL_SIZE = 4

class Color(IntEnum):
    BLUE = auto()
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    PURPLE = auto()
    ORANGE = auto()

    @classmethod
    def random_color(cls):
        return random.choice(list(cls))
        
        

class Pixel():

    def __init__(self, color, rgb, position):
        self.color = color
        self.rgb = rgb
        self.position = position # (x, y) tuple

# Tried to make a tetrominoe class but didn't really work
# class Tetrominoe():

#     def __init__(self, size):
#         # self.block = random.choice['O', 'L', 'J', 'T', 'I', 'S', 'Z']
#         self.block = 'T'
#         self.size = size
#         #sand will contain only the current sand pixels
#         self.sand = [[None for j in range(self.size[0])] for i in range(self.size[1])]

#     def draw_block(self):
#         block_color = Color.random_color()
#         color_rgb = {1: (53, 89, 144), 2: (164, 65, 47), 3: (97, 152, 74), 4: (204, 154, 52), 5: (145, 128, 196), 6: (255, 127, 39)}
#         if self.block == 'T':
#             for i in range(0, 12):
#                 for j in range(44, 56):
#                     self.sand[i][j] = Pixel(block_color, color_rgb[block_color], (j, i))
#             for i in range(12, 25):
#                 for j in range(32, 68):
#                     self.sand[i][j] = Pixel(block_color, color_rgb[block_color], (j, i))

class Tetris_Env():

    tetrominoe_set = set()

    def __init__(self, position, size):
        self.position = position
        self.size = size
        #sand will contain only the current sand pixels
        self.sand = [[None for j in range(self.size[0])] for i in range(self.size[1])]
        TETROMINOE_SIZE = 12 # even number please
        # default block:
        block_color = Color.random_color()
        color_rgb = {1: (53, 89, 144), 2: (164, 65, 47), 3: (97, 152, 74), 4: (204, 154, 52), 5: (145, 128, 196), 6: (255, 127, 39)}
        tetrominoe = random.choice(['O', 'L', 'J', 'T', 'I', 'S', 'Z'])
        if tetrominoe == 'O':
            for i in range(0, TETROMINOE_SIZE*2):
                for j in range(int(size[0]/2) - TETROMINOE_SIZE, int(size[0]/2) + TETROMINOE_SIZE):
                    self.sand[i][j] = Pixel(block_color, color_rgb[block_color], (j, i))
        elif tetrominoe == 'L':
            for i in range(0, TETROMINOE_SIZE*3):
                for j in range(int(size[0]/2) - TETROMINOE_SIZE, int(size[0]/2)):
                    self.sand[i][j] = Pixel(block_color, color_rgb[block_color], (j, i))
            for i in range(TETROMINOE_SIZE*2, TETROMINOE_SIZE*3):
                for j in range(int(size[0]/2), int(size[0]/2) + TETROMINOE_SIZE):
                    self.sand[i][j] = Pixel(block_color, color_rgb[block_color], (j, i))
        elif tetrominoe == 'J':
            for i in range(0, TETROMINOE_SIZE*3):
                for j in range(int(size[0]/2), int(size[0]/2) + TETROMINOE_SIZE):
                    self.sand[i][j] = Pixel(block_color, color_rgb[block_color], (j, i))
            for i in range(TETROMINOE_SIZE*2, TETROMINOE_SIZE*3):
                for j in range(int(size[0]/2) - TETROMINOE_SIZE, int(size[0]/2)):
                    self.sand[i][j] = Pixel(block_color, color_rgb[block_color], (j, i))
        elif tetrominoe == 'T':
            for i in range(0, TETROMINOE_SIZE):
                for j in range(int(size[0]/2) - int(TETROMINOE_SIZE/2), int(size[0]/2) + int(TETROMINOE_SIZE/2)):
                    self.sand[i][j] = Pixel(block_color, color_rgb[block_color], (j, i))
            for i in range(TETROMINOE_SIZE, (TETROMINOE_SIZE*2)+1):
                for j in range(int(size[0]/2) - int(TETROMINOE_SIZE*3/2), int(size[0]/2) + int(TETROMINOE_SIZE*3/2)):
                    self.sand[i][j] = Pixel(block_color, color_rgb[block_color], (j, i))
        elif tetrominoe == 'I':
            for i in range(0, TETROMINOE_SIZE*4):
                for j in range(int(size[0]/2) - int(TETROMINOE_SIZE/2), int(size[0]/2) + int(TETROMINOE_SIZE/2)):
                    self.sand[i][j] = Pixel(block_color, color_rgb[block_color], (j, i))
        elif tetrominoe == 'S':
            for i in range(0, TETROMINOE_SIZE):
                for j in range(int(size[0]/2) - int(TETROMINOE_SIZE/2), int(size[0]/2) + int(TETROMINOE_SIZE*3/2)):
                    self.sand[i][j] = Pixel(block_color, color_rgb[block_color], (j, i))
            for i in range(TETROMINOE_SIZE, TETROMINOE_SIZE*2):
                for j in range(int(size[0]/2) - int(TETROMINOE_SIZE*3/2), int(size[0]/2) + int(TETROMINOE_SIZE/2)):
                    self.sand[i][j] = Pixel(block_color, color_rgb[block_color], (j, i))
        elif tetrominoe == 'Z':
            for i in range(0, TETROMINOE_SIZE):
                for j in range(int(size[0]/2) - int(TETROMINOE_SIZE*3/2), int(size[0]/2) + int(TETROMINOE_SIZE/2)):
                    self.sand[i][j] = Pixel(block_color, color_rgb[block_color], (j, i))
            for i in range(TETROMINOE_SIZE, TETROMINOE_SIZE*2):
                for j in range(int(size[0]/2) - int(TETROMINOE_SIZE/2), int(size[0]/2) + int(TETROMINOE_SIZE*3/2)):
                    self.sand[i][j] = Pixel(block_color, color_rgb[block_color], (j, i))

        self.tetrominoe = None
        self.next_tetrominoe = None

    def reset(self):
        pass

    def get_state(self): # returns a np array that represents the board (a snapshot of where the current piece and sand are)
        # Boolean Channels for each color class (if this is too much, then lets do a rgb channel for the color classes and normalize them with 255)
        # 1) red
        # 2) blue
        # 3) green
        # 4) yellow
        # 5) 
        pass

    def step(self, action):

        def set_cell(x, y, pixel):
            self.sand[y][x] = pixel

        def empty(x, y):
            return x >= 0 and x < self.size[0] and y >= 0 and y < self.size[1] and self.sand[y][x] is None

        def update_cell(x, y):
            pixel = self.sand[y][x]

            down = empty(x, y+1)
            left = empty(x-1, y+1)
            right = empty(x+1, y+1)

            if left and right:
                rand = random.randint(0, 1) > 0.5
                left = rand
                right = not rand

            if down:
                set_cell(x, y+1, pixel)
            elif left:
                set_cell(x-1, y+1, pixel)
            elif right:
                set_cell(x+1, y+1, pixel)

            if down or left or right:
                set_cell(x, y, None)

        def check_match(): # this helper function will help find a connection path from both ends to determine a match ha sbeen made
            pass

        for y in range(self.size[1]-1, -1, -1):
            for x in range(self.size[0]-1, -1, -1):
                update_cell(x, y)
