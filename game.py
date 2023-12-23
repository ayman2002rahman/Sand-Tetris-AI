import pygame
import sys
from tetris_env import Tetris_Env, CELL_SIZE

DISPLAY_SIZE = (1000, 1000)
GAME_POSITION = (300, 200)
WIDTH = 100
HEIGHT = 160
BORDER_THICKNESS = 5

pygame.init()
screen = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption("Sand Tetris AI")
clock = pygame.time.Clock()

def draw_game(env):
    pygame.draw.rect(screen, (255, 255, 255), (env.position[0]-BORDER_THICKNESS, env.position[1]-BORDER_THICKNESS, 2*BORDER_THICKNESS+env.size[0]*CELL_SIZE, 2*BORDER_THICKNESS+env.size[1]*CELL_SIZE))
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

        screen.fill((0, 0, 0))
        draw_game(env)
        env.step(None)
        pygame.display.flip()
        #clock.tick(60)

if __name__ == '__main__':
    main()