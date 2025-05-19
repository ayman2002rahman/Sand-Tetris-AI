from enum import Enum
import random
from color import Color

class Tetromino_Shapes(Enum):
    I = [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    O = [
        [1, 1, 0],
        [1, 1, 0],
        [0, 0, 0],
    ]
    T = [
        [1, 1, 1],
        [0, 1, 0],
        [0, 0, 0],
    ]
    S = [
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0],
    ]
    Z = [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0],
    ]
    J = [
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
    ]
    L = [
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0],
    ]

    @classmethod
    def random_shape(cls):
        return random.choice(list(cls))

class Tetromino:
    def __init__(self, position, grid_width):
        self.position = position
        self.shape = Tetromino_Shapes.random_shape()
        for _ in range(random.randint(3)):
            self.rotate()
        self.color = Color.random_color()
        self.grid_width = grid_width

    # will need to add logic to ensure that tetromino after rotation does not exit side boundaries
    # while trtromino too far right, shift it left
    # while tetromino too far left, shift it right
    # check its left-msot and right most-cells
    def left_most_x(self):
        left_block = 0
        for block_x in range(len(self.shape[0])):
            for block_y in range(len(self.shape)):
                if self.shape[block_y][block_x]:
                    left_block = block_x
                    break
        return self.x + left_block * 8

    def right_most_x(self):
        right_block = 0
        for block_x in range(len(self.shape[0]), -1, -1):
            for block_y in range(len(self.shape)):
                if self.shape[block_y][block_x]:
                    right_block = block_x
                    break
        return self.x + right_block * 8 + 7

    def rotate(self):
        t = self.shape.copy()
        t = [list(row) for row in zip(*t[::-1])]
        self.shape = t.copy()

        right_x = self.right_most_x()
        if right_x >= self.grid_width:
            while right_x >= self.grid_width:
                self.x -= 1
                right_x -= 1
        else:
            left_x = self.left_most_x()
            while left_x < 0:
                self.x += 1
                left_x += 1

    def get_pixels(self):
        pixels = []
        for block_y, row in enumerate(self.shape):
            for block_x, cell in enumerate(row):
                if cell:
                    for dy in range(8):
                        for dx in range(8):
                            px = self.position[0] + block_x * 8 + dx
                            py = self.position[1] + block_y * 8 + dy
                            pixels.append((px, py))
        return pixels

