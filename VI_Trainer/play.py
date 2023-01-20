import numpy as np
import pygame
import game


class Play(game.GridWorld):

    def __init__(self, envi=None, table=None, size=None):
        super().__init__(envi=envi, table=table, size=size)
        ag_ta = self.get_ag_ta()
        self.agent = ag_ta[0]
        self.target = ag_ta[1]
        self.env = self.get_env()
        self.agent_start = self.agent.copy() if self.agent else False
        self.path = list()
        self.prepare()

    def play(self, visual=False, re=True, exit_window=True):
        pygame.display.set_caption(f"GridWorld {self.env_len}x{self.env_len}")
        if not self.agent or not self.target:
            self.run = False
        while self.run:
            state = self.reset()
            self.path.append(state)
            while not self.over:
                action = self.get_action(state)
                self.draw_border()
                if visual:
                    self.draw_game_visual(action)
                else:
                    self.draw_game_non_visual()
                state = self.move(action)
                self.path.append(state)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                        self.over = True
                keys = pygame.key.get_pressed()
                if keys[pygame.K_f]:
                    self.run = False
                    self.over = True
            if not re:
                self.run = False
        if exit_window:
            pygame.display.quit()

    def get_action(self, state):
        next_state = [[state[0]-1, state[1]], [state[0]+1, state[1]],
                      [state[0], state[1]-1], [state[0], state[1]+1]]
        vals = list()
        for i, item in enumerate(next_state):
            try:
                if item[0] >= 0 and item[1] >= 0:
                    vals.append(self.v_table[item[0]][item[1]])
                else:
                    vals.append(- self.env_len*self.env_len)
            except IndexError:
                vals.append(- self.env_len*self.env_len)
        return np.argmax(vals)

    def show_env(self):
        pygame.display.set_caption(f"GridWorld {self.env_len}x{self.env_len}")
        if self.agent:
            self.play(re=False, exit_window=False)
        self.run = True
        while self.run:
            self.draw_border()
            self.draw_board(path=self.path.copy())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_f]:
                self.run = False
                outer_run = False
        pygame.display.quit()
