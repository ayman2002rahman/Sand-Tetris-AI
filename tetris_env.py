import pygame
from color import Color
from tetromino import Tetromino
from enum import IntEnum, auto
import random

CELL_SIZE = 4
        
ACTIONS = [
    "right",
    "left",
    "down",
    "rotate",
    "none"
]

class Pixel():

    def __init__(self, color, color_class, position):
        self.color = color
        self.color_class = color_class
        self.position = position # (x, y) tuple

# also pass in seed to generate random tetrominos so two different envs can follow same tetromino sequence
class Tetris_Env():

    def __init__(self, position, size):
        self.position = position
        self.size = size # (width, height)
        #sand will contain only the current sand pixels
        self.sand = [[None for j in range(self.size[0])] for i in range(self.size[1])]
        
        self.tetromino = Tetromino((10, 0), self.size[0])
        self.next_tetromino = Tetromino((10, 0), self.size[0])
        self.score = 0

    def reset(self):
        pass

    def get_state(self): # returns a np array that represents the board (a snapshot of where the current piece and sand are)
        # Boolean Channels for each color class (if this is too much, then lets do a rgb channel for the color classes and normalize them with 255)
        # 1) red
        # 2) blue
        # 3) green
        # 4) yellow
        pass

    def pixel_at(self, x, y): # helper function to get the sandf pizxel at i=y and j=x
        return self.sand[y][x]

    def valid_actions(self):
        valid_actions = ["none", "rotate"]

        # check left
        left_x = self.tetromino.left_most_x()
        if left_x > 0:
            valid_actions.append('left')
        
        # check right
        right_x = self.tetromino.right_most_x()
        if right_x < self.size[0] - 1:
            valid_actions.append('right')

        # check down
        # def check_down():
        #     for x, y in self.tetromino.get_pixels():
        #         for dx, dy in [(0, 1)]:
        #             nx, ny = x + dx, y + dy
        #             if ny >= self.size[1]:
        #                 return True
        #         if 0 <= nx and nx < self.size[0] and self.pixel_at(nx, ny):
        #             return True
        #     return False

        return valid_actions

    def step(self, action):
        # 1.) handle action logic
        # 2.) Check tetromino collision
        # 3.) update sand physics 
        # 4.) check for a match

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
 
        def bfs(staring_y):
            match = False

            search_color = self.pixel_at(0, staring_y).color
            visited = set()
            queue = [(0, staring_y)] # stores x, y pairs to represent pixel's position
            while len(queue) > 0: # may need to change the logic if we append pixles to the queue and check their validitiy after they are popped from it (queue would be larger)
                x, y = queue.pop(0)

                # Check to see if pixel needs to be ignored
                if (
                    x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1] or # out of bounds
                    (x, y) in visited or # seen
                    self.pixel_at(x, y) is None or # no pixel
                    self.pixel_at(x, y).color is not search_color # wrong color
                ):
                    continue

                visited.add((x, y))

                # check for goal (if a connection has been made, then the goal will be a pixel on the right wall)
                if x == self.size[0]-1:
                    match = True

                # check all 4 directions
                queue.append((x, y-1)) # up 
                queue.append((x+1, y)) # right 
                queue.append((x, y+1)) # down 
                queue.append((x-1, y)) # left 

            if match:
                return visited
            else:
                return None

        def left_wall():
            wall = [] # from bottom to top, store the first i index for each unique color section
            current_color = None
            for y in range(self.size[1]-1, -1, -1):
                pixel = self.pixel_at(0, y)
                if pixel is None:
                    break
                if pixel.color is not current_color:
                    wall.append(y)
                    current_color = pixel.color
            return wall
                
        def collides():
            for x, y in self.tetromino.get_pixels():
                for dx, dy in [(0, 1), (-1, 0), (1, 0)]:
                    nx, ny = x + dx, y + dy
                    if ny >= self.size[1]:
                        return True
                if 0 <= nx and nx < self.size[0] and self.pixel_at(nx, ny):
                    return True
            return False
        
        def try_move(dx, dy):
            """Attempt to move by (dx,dy), revert and return False if colliding."""
            orig = self.tetromino.position
            new_pos = (orig[0] + dx, orig[1] + dy)
            self.tetromino.position = new_pos
            if collides():
                self.tetromino.position = orig
                return False
            return True
        
        # --- STEP FUNCTION LOGIC ---
        x, y = self.tetromino.position

        valid_actions = self.valid_actions()
        # determine deltas
        if action in valid_actions:
            if action == 'left':
                h_move = -2
                v_move = 1
            elif action == 'right':
                h_move = 2
                v_move = 1
            elif action == 'left-down':
                h_move = -2
                v_move = 1
            elif action == 'right-down':
                h_move = 2
                v_move = 1
            elif action == 'down':
                h_move = 0
                v_move = 1
            elif action == 'rotate':
                self.tetromino.rotate()
                h_move = 0
                v_move = 1
            else:
                h_move = 0
                v_move = 1
        else:
            h_move = 0
            v_move = 1

        # 1) Horizontal phase: try 2px, then 1px, then stay
        if h_move != 0:
            if not try_move(h_move, 0):
                sign = 1 if h_move > 0 else -1
                # fallback to 1px
                if not try_move(sign, 0):
                    # blocked: no horizontal move at all
                    pass

        # 2) Vertical phase: always try 1px down
        if not try_move(0, v_move):
            # collided downward → lock & spawn
            color   = self.tetromino.color
            grid_h  = len(self.sand)
            grid_w  = len(self.sand[0])
            # lock into sand exactly as before
            for by, row in enumerate(self.tetromino.shape):
                for bx, cell in enumerate(row):
                    if not cell: continue
                    base_x = self.tetromino.position[0] + bx * 8
                    base_y = self.tetromino.position[1] + by * 8
                    for dy in range(8):
                        for dx in range(8):
                            px = base_x + dx
                            py = base_y + dy
                            if 0 <= px < grid_w and 0 <= py < grid_h:
                                ring  = min(dx, 7-dx, dy, 7-dy)
                                shade = ["dark","medium","dark","light"][ring]
                                self.sand[py][px] = Pixel(color, shade, (px,py))
            # spawn next piece
            self.tetromino = Tetromino((10,0), self.size[0])


        # 2.) Check tetromino collision
        if collides():
            color = self.tetromino.color

            grid_h = len(self.sand)
            grid_w = len(self.sand[0])

            for block_y, row in enumerate(self.tetromino.shape):
                for block_x, cell in enumerate(row):
                    if not cell:
                        continue

                    base_x = self.tetromino.position[0] + block_x * 8
                    base_y = self.tetromino.position[1] + block_y * 8

                    for dy in range(8):
                        for dx in range(8):
                            px = base_x + dx
                            py = base_y + dy

                            # only lock into the sand grid if within bounds
                            if 0 <= px < grid_w and 0 <= py < grid_h:
                                ring = min(dx, 7 - dx, dy, 7 - dy)
                                shade = ["dark", "medium", "dark", "light"][ring]
                                self.sand[py][px] = Pixel(color, shade, (px, py))

            self.tetromino = Tetromino((10, 0), self.size[0])

                                

        # 3.) sand physics
        for y in range(self.size[1]-1, -1, -1): # bottom up
            for x in range(self.size[0]-1, -1, -1):
                update_cell(x, y)
        
        # 4.) check for a match (currently only handles one match at a time: does not handle if there are two matches made at the same exact time (very low chance))
        
        wall = left_wall()
        for starting_y in wall:
            visited = bfs(starting_y)
            if visited:
                print('match made')
                # delete the pixels
                for x, y in visited:
                    self.sand[y][x] = None
                # This score value will depend on how many pixels were made in the match
                self.score += 100 # add on score value of making a match
                return visited, False
            
        return None, False