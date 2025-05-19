from enum import IntEnum, auto
import random

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