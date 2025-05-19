import pygame
import sys
import time
from tetris_env import Tetris_Env, CELL_SIZE, ACTIONS
from color import Color

DISPLAY_SIZE = (1000, 1000)
GAME_POSITION = (150, 200)
WIDTH = 37
HEIGHT = 60
BORDER_THICKNESS = 5

FLICKER_FREQUENCY = 3

pygame.init()
screen = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption("Sand Tetris AI")
clock = pygame.time.Clock()

def draw_game(env):
    # background:
    for i in range(0, DISPLAY_SIZE[1], 100):
        for j in range(0, DISPLAY_SIZE[0], 100):
            pygame.draw.rect(screen, (232, 150, 101), (j, i, 50, 50))
            pygame.draw.rect(screen, (243, 184, 136), (j+50, i, 50, 50))
            pygame.draw.rect(screen, (243, 184, 136), (j, i+50, 50, 50))
            pygame.draw.rect(screen, (232, 150, 101), (j+50, i+50, 50, 50))
    # border:
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (
            env.position[0] - BORDER_THICKNESS,
            env.position[1] - BORDER_THICKNESS,
            2 * BORDER_THICKNESS + env.size[0] * CELL_SIZE,
            2 * BORDER_THICKNESS + env.size[1] * CELL_SIZE,
        ),
    )
    # playable area:
    pygame.draw.rect(
        screen,
        (0, 0, 0),
        (env.position[0], env.position[1], env.size[0] * CELL_SIZE, env.size[1] * CELL_SIZE),
    )

    # define a shared palette for each color's three shades
    shade_colors = {
        Color.BLUE:   {'dark': (0, 0, 150),   'medium': (0, 0, 255),   'light': (100, 100, 255)},
        Color.RED:    {'dark': (150, 0, 0),   'medium': (255, 0, 0),   'light': (255, 100, 100)},
        Color.GREEN:  {'dark': (0, 150, 0),   'medium': (0, 255, 0),   'light': (100, 255, 100)},
        Color.YELLOW: {'dark': (150, 150, 0), 'medium': (255, 255, 0), 'light': (255, 255, 150)},
    }

    # 1) draw sand using pixel.color_class
    for y in range(env.size[1]):
        for x in range(env.size[0]):
            pixel = env.sand[y][x]
            if pixel is not None:
                # look up the correct rgb by color and class
                rgb = shade_colors[pixel.color][pixel.color_class]
                pygame.draw.rect(
                    screen,
                    rgb,
                    (env.position[0] + x * CELL_SIZE,
                     env.position[1] + y * CELL_SIZE,
                     CELL_SIZE,
                     CELL_SIZE),
                )

    # 2) draw falling tetromino using same palette logic
    ring_shades = ['dark', 'medium', 'dark', 'light']
    for px, py in env.tetromino.get_pixels():
        local_dx = (px - env.tetromino.position[0]) % 8
        local_dy = (py - env.tetromino.position[1]) % 8
        ring = min(local_dx, 7 - local_dx, local_dy, 7 - local_dy)
        shade_key = ring_shades[ring]

        shade_rgb = shade_colors[env.tetromino.color][shade_key]
        screen_x = env.position[0] + px * CELL_SIZE
        screen_y = env.position[1] + py * CELL_SIZE

        pygame.draw.rect(
            screen,
            shade_rgb,
            (screen_x, screen_y, CELL_SIZE, CELL_SIZE),
        )

    
def draw_match_visual(env, visited):
    for x, y in visited:
        pygame.draw.rect(screen, (255, 255, 255), (env.position[0]+x*CELL_SIZE, env.position[1]+y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def override_match_visual(env, visited):
    for x, y in visited:
        pygame.draw.rect(screen, (0, 0, 0), (env.position[0]+x*CELL_SIZE, env.position[1]+y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    env = Tetris_Env(GAME_POSITION, (WIDTH, HEIGHT))

    flickering = False
    visited = None
    flick_frame = 3
    flicks = 0
    draw_white = False

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_game(env)

        if not flickering:
            visited = env.step('right')
            if visited:
                flickering = True
        else:
            if flicks <= FLICKER_FREQUENCY:
                if draw_white:
                    draw_match_visual(env, visited)
                    flick_frame -= 1
                    if flick_frame <= 0:
                        flick_frame = 3
                        draw_white = False
                else:
                    override_match_visual(env, visited)
                    flick_frame -= 1
                    if flick_frame <= 0:
                        flick_frame = 3
                        draw_white = True
                        flicks += 1
            else:
                flicks = 0
                flickering = False

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()