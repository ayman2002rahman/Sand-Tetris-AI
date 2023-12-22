import pygame
from enum import IntEnum, auto
import random
import numpy as np

WIDTH = 500
HEIGHT = 1000
CELL_SIZE = 10

class Color(IntEnum):
    BLUE = auto()
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    PURPLE = auto()
    ORANGE = auto()

class Pixel():

    def __init__(self, color, rgb, position):
        self.color = color
        self.rgb = rgb
        self.position = position # (x, y) tuple

class Tetris_Env():

    def __init__(self):
        #sand will contain only the current sand pixels
        self.sand = [[None for j in range(WIDTH)] for i in range(HEIGHT)]
        for i in range(0, 100, 2):
            for j in range(0, 50, 2):
                self.sand[i][j] = Pixel(Color.BLUE, (0, 0, 255), (j, i))

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
            return x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT and self.sand[y][x] is None

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

        for y in range(HEIGHT-1, -1, -1):
            for x in range(WIDTH-1, -1, -1):
                update_cell(x, y)
