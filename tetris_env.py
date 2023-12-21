from enum import IntEnum, auto
import random

WIDTH = 50
HEIGHT = 200

class Color(IntEnum):
    BLUE = auto()
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    PURPLE = auto()
    ORANGE = auto()

class Tetris_Env():

    def __init__(self):
        #sand will contain only the current sand pixels
        self.sand = [[0 for j in range(WIDTH)] for i in range(HEIGHT)]

    def reset(self):
        pass

    def get_state(self):
        pass

    def step(self):

        def update_cell(x, y):
            self.sand[x][y] = self.sand[x][y+1]

        for x in range(HEIGHT-1, -1, -1):
            for y in range(WIDTH-1, -1, -1):
                update_cell(x, y)

    def get_board(self):
        return self.sand