import pygame
import numpy as np


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (34, 177, 76)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

WIDTH_MAX = 600

a = np.load("env-14x14-33.npy")

VEL = WIDTH_MAX // len(a)

SHAPE = VEL - 1
WIDTH = VEL * len(a) + 1
HEIGHT = WIDTH


def draw_board():
    for i in range(len(a)+1):
                pygame.draw.line(win, WHITE, (i*VEL, 0), (i*VEL, VEL*len(a)))
                pygame.draw.line(win, WHITE, (0, i*VEL), (VEL*len(a), i*VEL))
    for i in range(len(a)):
        for j in range(len(a)):
            if a[i][j] == 99:
                pygame.draw.rect(win, RED, (VEL*j+1, VEL*i+1, SHAPE, SHAPE))
            elif a[i][j] == 1:
                pygame.draw.rect(win, YELLOW, (VEL*j+1,
                                                    VEL*i+1, SHAPE, SHAPE))
            elif a[i][j] == 2:
                pygame.draw.rect(win, GREEN, (VEL*j+1,
                                                   VEL*i+1, SHAPE, SHAPE))


pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode((WIDTH, HEIGHT))
game = True

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    win.fill(BLACK)
    # Boundary
    draw_board()

    pygame.display.flip()
    clock.tick(60)
