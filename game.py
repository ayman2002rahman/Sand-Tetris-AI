import pygame
import sys
import time
from tetris_env import Tetris_Env, CELL_SIZE

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
    pygame.draw.rect(screen, (255, 255, 255), (env.position[0]-BORDER_THICKNESS, env.position[1]-BORDER_THICKNESS, 2*BORDER_THICKNESS+env.size[0]*CELL_SIZE, 2*BORDER_THICKNESS+env.size[1]*CELL_SIZE))
    # playable area:
    pygame.draw.rect(screen, (0, 0, 0), (env.position[0], env.position[1], env.size[0]*CELL_SIZE, env.size[1]*CELL_SIZE))
    
    # sand
    for y in range(env.size[1]):
        for x in range(env.size[0]):
            if env.sand[y][x] is not None:
                pixel = env.sand[y][x]
                pygame.draw.rect(screen, pixel.rgb, (env.position[0]+x*CELL_SIZE, env.position[1]+y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # tetromino
    
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
            visited = env.step(None)
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