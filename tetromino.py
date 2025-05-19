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
    def __init__(self, position):
        self.position = position
        self.shape = Tetromino_Shapes.random_shape()
        for _ in range(random.randint(3)):
            self.rotate()
        self.color = Color.random_color()

    # will need to add logic to ensure that tetromino after rotation does not exit side boundaries
    # while trtromino too far right, shift it left
    # while tetromino too far left, shift it right
    # check its left-msot and right most-cells
    def rotate(self):
        t = self.shape.copy()
        t = [list(row) for row in zip(*t[::-1])]
        self.shape = t.copy()

    def get_pixels(self):
        pixels = []
        for block_y, row in enumerate(self.shape):
            for block_x, cell in enumerate(row):
                if cell:
                    for dy in range(8):
                        for dx in range(8):
                            px = self.x + block_x * 8 + dx
                            py = self.y + block_y * 8 + dy
                            pixels.append((px, py))
        return pixels

