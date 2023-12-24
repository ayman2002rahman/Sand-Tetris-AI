import pygame
import sys
from tetris_env import Tetris_Env, CELL_SIZE

DISPLAY_SIZE = (1000, 1000)
GAME_POSITION = (150, 200)
WIDTH = 100
HEIGHT = 160
BORDER_THICKNESS = 5

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
    for y in range(env.size[1]):
        for x in range(env.size[0]):
            if env.sand[y][x] is not None:
                pixel = env.sand[y][x]
                pygame.draw.rect(screen, pixel.rgb, (env.position[0]+x*CELL_SIZE, env.position[1]+y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    env = Tetris_Env(GAME_POSITION, (WIDTH, HEIGHT))

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_game(env)
        env.step(None)
        pygame.display.flip()
        #clock.tick(60)

if __name__ == '__main__':
    main()