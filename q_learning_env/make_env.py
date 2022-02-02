import numpy as np
import pygame
import os


def clear():
    os.system("cls")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (34, 177, 76)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

AGENT = 1
TREASURE = 2
HOLE = 99

WIDTH_MAX = 600


shape = int(input("enter env shape:"))

VEL = WIDTH_MAX // shape

SHAPE = VEL - 1
WIDTH = VEL * shape + 1
HEIGHT = WIDTH

ENV = np.zeros((shape, shape))

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 40)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Make Env")
choice = HOLE
is_agent_placed = False
is_treasure_placed = False
hole_count = 0


def draw_board():
    for i in range(shape+1):
        pygame.draw.line(win, WHITE, (i*VEL, 0), (i*VEL, VEL*shape))
        pygame.draw.line(win, WHITE, (0, i*VEL), (VEL*shape, i*VEL))
    for i in range(shape):
        for j in range(shape):
            if ENV[i][j] == AGENT:
                pygame.draw.rect(win, YELLOW, (VEL*j+1, VEL*i+1, SHAPE, SHAPE))
            elif ENV[i][j] == HOLE:
                pygame.draw.rect(win, RED, (VEL*j+1, VEL*i+1, SHAPE, SHAPE))
            elif ENV[i][j] == TREASURE:
                pygame.draw.rect(win, GREEN, (VEL*j+1, VEL*i+1, SHAPE, SHAPE))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            cursor_pos = event.pos
            x = int(np.floor(cursor_pos[0] / VEL))
            y = int(np.floor(cursor_pos[1] / VEL))
            if choice == AGENT and not is_agent_placed:
                if ENV[y][x] > 0:
                    pass
                else:
                    ENV[y][x] = AGENT
                    is_agent_placed = True
            elif choice == HOLE:
                if ENV[y][x] > 0:
                    pass
                else:
                    ENV[y][x] = HOLE
                    hole_count += 1
            elif choice == TREASURE and not is_treasure_placed:
                if ENV[y][x] > 0:
                    pass
                else:
                    ENV[y][x] = TREASURE
                    is_treasure_placed = True
            clear()
            print(ENV)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                if not is_agent_placed:
                    choice = AGENT
            elif event.key == pygame.K_f:
                choice = HOLE
            elif event.key == pygame.K_d:
                if not is_treasure_placed:
                    choice = TREASURE
            elif event.key == pygame.K_r:
                ENV = np.zeros((shape, shape))
                hole_count = 0
                is_agent_placed = False
                is_treasure_placed = False
            elif event.key == pygame.K_q:
                poss = pygame.mouse.get_pos()
                x = int(np.floor(poss[0] / VEL))
                y = int(np.floor(poss[1] / VEL))
                if ENV[y][x] == HOLE:
                    ENV[y][x] = 0
                    hole_count -= 1
                elif ENV[y][x] == AGENT:
                    ENV[y][x] = 0
                    is_agent_placed = False
                elif ENV[y][x] == TREASURE:
                    ENV[y][x] = 0
                    is_treasure_placed = False
            elif event.key == pygame.K_s:
                if is_agent_placed and is_treasure_placed and hole_count > 0:
                    np.save("env", ENV)
                    quit()
                else:
                    print("Please place holes and goal")
    win.fill(BLACK)
    draw_board()
    count = font.render(f"{hole_count}", 1, BLUE)
    win.blit(count, (0, 0))
    pygame.display.flip()
    clock.tick(60)
