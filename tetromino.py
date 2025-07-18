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
        shape_enum = Tetromino_Shapes.random_shape()
        self.shape = [row[:] for row in shape_enum.value]
        self.grid_width = grid_width
        self.color = Color.random_color()
        for _ in range(random.randint(0, 3)):
            self.rotate()

    # will need to add logic to ensure that tetromino after rotation does not exit side boundaries
    # while trtromino too far right, shift it left
    # while tetromino too far left, shift it right
    # check its left-msot and right most-cells
    def left_most_x(self):
        left_block = 2
        for block_x in range(len(self.shape[0])):
            for block_y in range(len(self.shape)):
                if self.shape[block_y][block_x]:
                    left_block = min(left_block, block_x)
        return self.position[0] + (left_block - 0)* 8

    def right_most_x(self):
        right_block = 0
        for block_x in range(len(self.shape[0])-1, -1, -1):
            for block_y in range(len(self.shape)):
                if self.shape[block_y][block_x]:
                    right_block = max(right_block, block_x)
        return self.position[0] + right_block * 8 + 7

    def rotate(self):
        t = self.shape
        t = [list(row) for row in zip(*t[::-1])]
        self.shape = t

        right_x = self.right_most_x()
        if right_x >= self.grid_width:
            while right_x >= self.grid_width:
                x, y = self.position
                self.position = (x - 1, y)
                right_x -= 1
        else:
            left_x = self.left_most_x()
            while left_x < 0:
                x, y = self.position
                self.position = (x + 1, y)
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

