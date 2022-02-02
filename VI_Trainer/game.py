import pygame
import numpy as np
import game_util as util

from game_items import *


class GridWorld:

    def __init__(self, envi=None, table=None, size=None):

        # Env
        self.envi = envi
        self.v_table = table
        self.env_len = size
        self.vel = WIDTH_MAX // self.env_len
        self.shape = self.vel - 1
        self.width = self.vel * self.env_len + 1
        self.height = self.width
        self.agent = None
        self.target = None
        self.agent_start = None

        self.img = util.Image()
        self.wheelImg_u = None
        self.wheelImg_d = None
        self.wheelImg_l = None
        self.wheelImg_r = None
        self.floor = None
        self.wall = None
        self.star = None

        # Game
        self.run = True
        self.game_flip = True
        self.over = False
        self.fps = FPS
        self.clock = pygame.time.Clock()

        self.win = pygame.display.set_mode((self.width, self.height))

    def prepare(self):
        try:
            self.wheelImg_u = self.img.load(WHEEL_UP_RE)
            self.wheelImg_r = self.img.load(WHEEL_RIGHT_RE)
            self.wheelImg_d = self.img.load(WHEEL_DOWN_RE)
            self.wheelImg_l = self.img.load(WHEEL_LEFT_RE)
            self.floor = self.img.load(HOUSE_RE)
            self.star = self.img.load(STAR_RE)
            self.wall = self.img.load(WALL_RE)
        except pygame.error:
            self.wheelImg_u = self.img.process(img_path=WHEEL_UP,
                                               dim=(self.shape, self.shape),
                                               save=True,
                                               save_path=WHEEL_UP_RE)
            self.wheelImg_r = self.img.process(img_path=WHEEL_RIGHT,
                                               dim=(self.shape, self.shape),
                                               save=True,
                                               save_path=WHEEL_RIGHT_RE)
            self.wheelImg_d = self.img.process(img_path=WHEEL_DOWN,
                                               dim=(self.shape, self.shape),
                                               save=True,
                                               save_path=WHEEL_DOWN_RE)
            self.wheelImg_l = self.img.process(img_path=WHEEL_LEFT,
                                               dim=(self.shape, self.shape),
                                               save=True,
                                               save_path=WHEEL_LEFT_RE)
            self.floor = self.img.process(img_path=HOUSE,
                                          dim=(self.width, self.height),
                                          save=True,
                                          save_path=HOUSE_RE)
            self.star = self.img.process(img_path=STAR,
                                         dim=(self.shape, self.shape),
                                         save=True,
                                         save_path=STAR_RE)
            self.wall = self.img.process(img_path=WALL,
                                         dim=(self.shape, self.shape),
                                         save=True,
                                         save_path=WALL_RE)

    def move(self, action):
        if action == UP:
            self.agent[0] -= 1
        elif action == DOWN:
            self.agent[0] += 1
        elif action == RIGHT:
            self.agent[1] += 1
        elif action == LEFT:
            self.agent[1] -= 1
        if self.agent[0] < 0 or self.agent[1] < 0 or self.agent[0] >\
                self.env_len-1 or self.agent[1] > self.env_len-1:
            self.over = True
        elif self.env[self.agent[0]][self.agent[1]] == TARGET:
            self.over = True
        elif self.env[self.agent[0]][self.agent[1]] == HOLE:
            self.over = True
        return self.agent.copy()

    def get_ag_ta(self):
        agent = []
        target = []
        agent_found = False
        target_found = False
        for i in range(self.env_len):
            for j in range(self.env_len):
                if self.envi[i][j] == AGENT:
                    agent = [i, j]
                    agent_found = True
                elif self.envi[i][j] == TARGET:
                    target = [i, j]
                    target_found = True
                else:
                    pass
        if not agent_found and not target_found:
            return False, False
        if not agent_found:
            return False, target.copy()
        else:
            return agent.copy(), target.copy()

    def get_env(self):
        if self.agent:
            env = self.envi.copy()
            env[self.agent[0]][self.agent[1]] = 0
            return env
        else:
            return self.envi

    def reset(self):
        self.over = False
        if self.agent:
            self.agent = self.agent_start.copy()
            return self.agent.copy()
        else:
            return False

    def draw_border(self, bg=BLACK, fg=WHITE):
        if self.game_flip:
            if bg:
                self.win.fill(bg)
            for i in range(self.env_len+1):
                pygame.draw.line(self.win, fg, (i*self.vel, 0),
                                 (i*self.vel, self.env_len*self.vel))
                pygame.draw.line(self.win, fg, (0, i*self.vel),
                                 (self.env_len*self.vel, i*self.vel))

    def draw_game_non_visual(self):
        if self.game_flip:
            for i in range(self.env_len):
                for j in range(self.env_len):
                    if self.env[i][j] == HOLE:
                        pygame.draw.rect(self.win, RED,
                                         (self.vel*j+1, self.vel*i+1,
                                          self.shape, self.shape))
            if self.agent:
                pygame.draw.rect(self.win, YELLOW,
                                 (self.vel*self.agent[1]+1,
                                  self.vel*self.agent[0]+1,
                                  self.shape, self.shape))
            if self.target:
                pygame.draw.rect(self.win, GREEN,
                                 (self.vel*self.target[1]+1,
                                  self.vel*self.target[0]+1,
                                  self.shape, self.shape))
            pygame.display.flip()
            self.clock.tick(self.fps)

    def draw_game_visual(self, dirr):
        if self.game_flip:
            start_pos = [self.agent[0]*self.vel+1, self.agent[1]*self.vel+1]
            for frame in range(int(self.vel/DRAW_VEL)):
                self.win.blit(self.floor, (0, 0))
                """
                self.draw_border(bg=False)
                for i in range(self.env_len):
                    for j in range(self.env_len):
                        if self.env[i][j] == 99:
                            self.win.blit(self.wall,
                                          (self.vel*j+1, self.vel*i+1))
                """
                self.win.blit(self.star, (self.vel*self.target[1]+1,
                                          self.vel*self.target[0]+1))
                if dirr == UP:
                    self.win.blit(self.wheelImg_u,
                                  (start_pos[1], start_pos[0]))
                    start_pos[0] -= DRAW_VEL
                elif dirr == RIGHT:
                    self.win.blit(self.wheelImg_r,
                                  (start_pos[1], start_pos[0]))
                    start_pos[1] += DRAW_VEL
                elif dirr == DOWN:
                    self.win.blit(self.wheelImg_d,
                                  (start_pos[1], start_pos[0]))
                    start_pos[0] += DRAW_VEL
                elif dirr == LEFT:
                    self.win.blit(self.wheelImg_l,
                                  (start_pos[1], start_pos[0]))
                    start_pos[1] -= DRAW_VEL
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                        self.over = True
                keys = pygame.key.get_pressed()
                if keys[pygame.K_f]:
                    self.run = False
                    self.over = True
                pygame.display.flip()
                self.clock.tick(self.fps)

    def draw_board(self, path=False, re=False):
        if self.game_flip:
            for i in range(self.env_len):
                for j in range(self.env_len):
                    if self.envi[i][j] == TARGET:
                        pygame.draw.rect(self.win, GREEN,
                                         (self.vel*j+1, self.vel*i+1,
                                          self.shape+1*re, self.shape+1*re))
                    elif self.envi[i][j] == HOLE:
                        pygame.draw.rect(self.win, RED,
                                         (self.vel*j+1, self.vel*i+1,
                                          self.shape+1*re, self.shape+1*re))
                    if self.envi[i][j] == AGENT:
                        pygame.draw.rect(self.win, YELLOW,
                                         (self.vel*j+1, self.vel*i+1,
                                          self.shape+1*re, self.shape+1*re))
            if path:
                div = 2
                en = 0
                pl = len(path)
                for ind, item in enumerate(path):
                    pygame.draw.rect(self.win, (255*(pl-ind)/pl,
                                                255, 255*(pl-ind)/pl),
                                     (self.vel*item[1]+1+self.shape/div/2*en,
                                      self.vel*item[0]+1+self.shape/div/2*en,
                                      self.shape-self.shape/div*en+1,
                                      self.shape-self.shape/div*en+1))
            pygame.display.flip()
            self.clock.tick(self.fps)
