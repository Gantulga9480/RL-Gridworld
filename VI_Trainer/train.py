import numpy as np
import game as game


class Train(game.GridWorld):

    def __init__(self, envi=None, table=None, size=None):
        super().__init__(envi=envi, table=table, size=size)
        font_size = np.int(self.shape - np.sqrt(2*(self.shape/3)**2))
        self.font1 = game.pygame.font.SysFont("arial", font_size)
        self.gamma = game.GAMMA
        self.P = game.TRANSITIONS
        self.hole_reward = - self.env_len * self.env_len
        self.target_reward = - self.hole_reward // 2
        self.empty_step_reward = 0  # self.hole_reward // 40 / 2
        ag_ta = self.get_ag_ta()
        self.agent = ag_ta[0]
        self.target = ag_ta[1]
        self.env = self.get_env()

    def get_state_val(self, state_):
        next_state = [[state_[0]-1, state_[1]], [state_[0], state_[1]+1],
                      [state_[0], state_[1]-1], [state_[0]+1, state_[1]]]
        vals = list()
        for i, item in enumerate(next_state):
            try:
                if item[0] >= 0 and item[1] >= 0:
                    vals.append(self.empty_step_reward + self.gamma *
                                self.v_table[item[0]][item[1]]*self.P[i])
                else:
                    pass
            except IndexError:
                pass
        return max(vals)

    def train(self):
        for i in range(self.env_len):
            for j in range(self.env_len):
                if self.env[i][j] == game.HOLE:
                    self.v_table[i][j] = self.hole_reward
                elif self.env[i][j] == game.TARGET:
                    self.v_table[i][j] = self.target_reward
        start_table = self.v_table.copy()
        temp_value = start_table.copy()
        run = True
        # for _ in range(self.env_len):
        while run:
            run = self.show_table()
            if run:
                for i in range(self.env_len):
                    for j in range(self.env_len):
                        if self.env[i][j] == game.HOLE:
                            pass
                        elif self.env[i][j] == game.TARGET:
                            pass
                        else:
                            temp_value[i][j] = self.get_state_val([i, j])
                self.v_table = temp_value.copy()
                temp_value = start_table.copy()
        np.save("v_table.npy", self.v_table)
        game.pygame.display.quit()

    def show_table(self):
        game.pygame.display.set_caption("v_table")
        show = True
        outer_run = True
        while show:
            for event in game.pygame.event.get():
                if event.type == game.pygame.QUIT:
                    show = False
                    outer_run = False
                keys = game.pygame.key.get_pressed()
                if keys[game.pygame.K_SPACE]:
                    show = False
                elif keys[game.pygame.K_f]:
                    show = False
                    outer_run = False
            self.win.fill(game.WHITE)
            self.draw_table(True)
            self.draw_border(bg=False, fg=game.BLACK)
            game.pygame.display.flip()
            self.clock.tick(self.fps)
        return outer_run

    def draw_table(self, num):
        for i in range(self.env_len):
            for j in range(self.env_len):
                score = self.v_table[i][j]
                if self.env[i][j] == game.TARGET:
                    game.pygame.draw.rect(self.win, game.GREEN,
                                          (self.vel*j+1, self.vel*i+1,
                                           self.vel, self.vel))
                elif self.env[i][j] == game.HOLE:
                    game.pygame.draw.rect(self.win, game.RED,
                                          (self.vel*j+1, self.vel*i+1,
                                           self.vel, self.vel))
                elif score == 0:
                    game.pygame.draw.rect(self.win, game.WHITE,
                                          (self.vel*j+1, self.vel*i+1,
                                           self.vel, self.vel))
                else:
                    if score < 0:
                        if np.abs(score)/self.target_reward >= 1:
                            game.pygame.draw.rect(self.win, game.BLUE,
                                                  (self.vel*j+1, self.vel*i+1,
                                                   self.vel, self.vel))
                        else:
                            color = 1 - np.abs(score)/self.target_reward
                            game.pygame.draw.rect(self.win, (255*color,
                                                             255*color,
                                                             255),
                                                  (self.vel*j+1, self.vel*i+1,
                                                   self.vel, self.vel))
                    else:
                        color = 1 - score/self.target_reward
                        game.pygame.draw.rect(self.win, (255*color,
                                                         255,
                                                         255*color),
                                              (self.vel*j+1, self.vel*i+1,
                                               self.vel, self.vel))
                if num:
                    if 0 < np.abs(score)-np.floor(np.abs(score)) < 1:
                        string1 = f"{np.round(score, 2)}"
                    else:
                        string1 = f"{int(score)}"
                    s = self.font1.render(string1, 1, game.BLACK)
                    self.win.blit(s, (j*self.vel+5, i*self.vel+5))
