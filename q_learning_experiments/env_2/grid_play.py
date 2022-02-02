import numpy as np
import time
import os
import pygame


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

a = np.load("env-8x8-11.npy")

LEN = len(a)
VEL = WIDTH_MAX // LEN

SHAPE = VEL - 1
WIDTH = VEL * LEN + 1
HEIGHT = WIDTH


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

    def draw_game(self):
        for i in range(LEN+1):
            pygame.draw.line(self.win, WHITE, (i*VEL, 0), (i*VEL, LEN*VEL))
            pygame.draw.line(self.win, WHITE, (0, i*VEL), (LEN*VEL, i*VEL))
        for i in range(LEN):
            for j in range(LEN):
                if self.env[i][j] == 99:
                    pygame.draw.rect(self.win, RED,
                                     (VEL*j+1, VEL*i+1, SHAPE, SHAPE))
        pygame.draw.rect(self.win, YELLOW,
                         (VEL*self.agent[1]+1,
                          VEL*self.agent[0]+1, SHAPE, SHAPE))
        pygame.draw.rect(self.win, GREEN,
                         (VEL*self.target[1]+1,
                          VEL*self.target[0]+1, SHAPE, SHAPE))

    def reset(self):
        self.agent = self.agent_start.copy()
        return self.agent.copy()

    def move(self, action):
        over = False
        self.win.fill(BLACK)
        self.draw_game()
        pygame.display.flip()
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                quit()
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
