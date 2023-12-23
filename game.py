import pygame
import sys
from tetris_env import Tetris_Env, HEIGHT, WIDTH, CELL_SIZE

DISPLAY_SIZE = (1000, 1000)

pygame.init()
screen = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption("Sand Tetris AI")
clock = pygame.time.Clock()

def draw_game(env):
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH*CELL_SIZE, HEIGHT*CELL_SIZE))
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if env.sand[y][x] is not None:
                pixel = env.sand[y][x]
                pygame.draw.rect(screen, pixel.rgb, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    env = Tetris_Env()

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