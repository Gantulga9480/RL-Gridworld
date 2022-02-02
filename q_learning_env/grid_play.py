import numpy as np
import os
import pygame
import cv2


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (34, 177, 76)
BLUE = (255, 0, 255)
YELLOW = (255, 255, 0)

WIDTH_MAX = 600

AGENT = 1
TARGET = 2
HOLE = 99

a = np.load("env.npy")

LEN = len(a)
VEL = WIDTH_MAX // LEN

SHAPE = VEL - 1
WIDTH = VEL * LEN + 1
HEIGHT = WIDTH
DRAW_VEL = 4
FPS = 60


try:
    carImg_up = pygame.image.load("img\\down_up.png")
    carImg_right = pygame.image.load("img\\down_right.png")
    carImg_down = pygame.image.load("img\\down_down.png")
    carImg_left = pygame.image.load("img\\down_left.png")
    floor = pygame.image.load("img\\grass_down.jpg")
    wall = pygame.image.load("img\\wall_down.jpg")
    star = pygame.image.load("img\\star_down.jpg")
except FileNotFoundError:
    carImg_up = cv2.imread("img\\wheel_1_up.png", cv2.IMREAD_UNCHANGED)
    carImg_right = cv2.imread("img\\wheel_1_right.png", cv2.IMREAD_UNCHANGED)
    carImg_down = cv2.imread("img\\wheel_1_down.png", cv2.IMREAD_UNCHANGED)
    carImg_left = cv2.imread("img\\wheel_1_left.png", cv2.IMREAD_UNCHANGED)
    floor = cv2.imread("img\\grass.jpg", cv2.IMREAD_UNCHANGED)
    wall = cv2.imread("img\\wall.jpg", cv2.IMREAD_UNCHANGED)
    star = cv2.imread("img\\star.png", cv2.IMREAD_UNCHANGED)

    dim = (SHAPE, SHAPE)
    floor_dim = (WIDTH, HEIGHT)
    wall_dim = (SHAPE, SHAPE)

    resized_up = cv2.resize(carImg_up, dim, interpolation=cv2.INTER_AREA)
    resized_right = cv2.resize(carImg_right, dim, interpolation=cv2.INTER_AREA)
    resized_down = cv2.resize(carImg_down, dim, interpolation=cv2.INTER_AREA)
    resized_left = cv2.resize(carImg_left, dim, interpolation=cv2.INTER_AREA)
    resized_floor = cv2.resize(floor, floor_dim, interpolation=cv2.INTER_AREA)
    resized_wall = cv2.resize(wall, wall_dim, interpolation=cv2.INTER_AREA)
    resized_star = cv2.resize(star, wall_dim, interpolation=cv2.INTER_AREA)

    cv2.imwrite("img\\down_up.png", resized_up)
    cv2.imwrite("img\\down_right.png", resized_right)
    cv2.imwrite("img\\down_down.png", resized_down)
    cv2.imwrite("img\\down_left.png", resized_left)
    cv2.imwrite("img\\grass_down.jpg", resized_floor)
    cv2.imwrite("img\\wall_down.jpg", resized_wall)
    cv2.imwrite("img\\star_down.png", resized_star)

    carImg_up = pygame.image.load("img\\down_up.png")
    carImg_right = pygame.image.load("img\\down_right.png")
    carImg_down = pygame.image.load("img\\down_down.png")
    carImg_left = pygame.image.load("img\\down_left.png")
    floor = pygame.image.load("img\\grass_down.jpg")
    wall = pygame.image.load("img\\wall_down.jpg")
    star = pygame.image.load("img\\star_down.png")


def clear():
    os.system("cls")


class GridWorld:

    def __init__(self, env, agent, target):
        self.env = env
        self.agent = agent
        self.agent_start = agent
        self.target = target
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.q_table = np.load("q_table.npy")

    def play(self):
        while True:
            over = False
            state = self.reset()
            actions = 0
            while not over:
                action = np.argmax(self.q_table[state[0]][state[1]])
                state, over = self.move(action)
                actions += 1
            if self.target[0] == self.agent[0] and\
                    self.target[1] == self.agent[1]:
                print("Won", actions)
            else:
                print("Over")

    def draw_game(self, dirr, start, stop):
        start_pos = [start[0]*VEL+1, start[1]*VEL+1]
        for frame in range(int(VEL/DRAW_VEL)):
            self.win.blit(floor, (0, 0))
            for i in range(LEN+1):
                pygame.draw.line(self.win, WHITE, (i*VEL, 0), (i*VEL, LEN*VEL))
                pygame.draw.line(self.win, WHITE, (0, i*VEL), (LEN*VEL, i*VEL))
            for i in range(LEN):
                for j in range(LEN):
                    if self.env[i][j] == 99:
                        self.win.blit(wall, (VEL*j+1, VEL*i+1))
            """
            pygame.draw.rect(self.win, YELLOW,
                             (start_pos[1],
                              start_pos[0], SHAPE, SHAPE))
            """
            self.win.blit(star, (VEL*self.target[1]+1, VEL*self.target[0]+1))
            if dirr == 0:
                self.win.blit(carImg_up,
                              (start_pos[1], start_pos[0]))
                start_pos[0] -= DRAW_VEL
            elif dirr == 2:
                self.win.blit(carImg_right,
                              (start_pos[1], start_pos[0]))
                start_pos[1] += DRAW_VEL
            elif dirr == 1:
                self.win.blit(carImg_down,
                              (start_pos[1], start_pos[0]))
                start_pos[0] += DRAW_VEL
            elif dirr == 3:
                self.win.blit(carImg_left,
                              (start_pos[1], start_pos[0]))
                start_pos[1] -= DRAW_VEL
            pygame.display.flip()
            clock.tick(FPS)

    def reset(self):
        self.agent = self.agent_start.copy()
        return self.agent.copy()

    def move(self, action):
        over = False
        start = [self.agent[0], self.agent[1]]
        if action == 0:
            self.agent[0] -= 1
        elif action == 1:
            self.agent[0] += 1
        elif action == 2:
            self.agent[1] += 1
        elif action == 3:
            self.agent[1] -= 1
        if self.agent[0] < 0 or self.agent[1] < 0 or self.agent[0] >\
                LEN-1 or self.agent[1] > LEN-1:
            over = True
        elif self.agent[0] == self.target[0] and\
                self.agent[1] == self.target[1]:
            over = True
        elif self.env[self.agent[0]][self.agent[1]] == 99:
            over = True
        else:
            pass
        stop = [self.agent[0], self.agent[1]]
        self.draw_game(action, start, stop)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        return self.agent.copy(), over


def get_agent_target(env):
    agent = []
    target = []
    for i in range(LEN):
        for j in range(LEN):
            if env[i][j] == AGENT:
                agent = [i, j]
            elif env[i][j] == TARGET:
                target = [i, j]
            else:
                pass
    return agent.copy(), target.copy()


def get_env(env, agent, target):
    env[agent[0]][agent[1]] = 0
    env[target[0]][target[1]] = 0
    return env


pygame.init()
pygame.display.set_caption("Simple GridWorld")
clock = pygame.time.Clock()
ag, ta = get_agent_target(a)
envi = get_env(a, ag.copy(), ta.copy())
env = GridWorld(envi, ag.copy(), ta.copy())
env.play()
