import numpy as np
import game as game


class Create(game.GridWorld):

    def __init__(self, envi=None, table=None, size=None):
        super().__init__(envi=envi, table=table, size=size)
        self.font = game.pygame.font.SysFont("arial", 40)
        self.choice = game.HOLE
        self.is_agent_placed = False
        self.is_treasure_placed = False
        self.hole_count = 0
        self.envi_len = size

    def get_cursor_pos(self, pos):
        x = int(np.floor(pos[0] / self.vel))
        y = int(np.floor(pos[1] / self.vel))
        return [x, y]

    def create_env(self):
        self.envi = np.zeros((self.envi_len, self.envi_len))
        self.v_table = np.zeros((self.envi_len, self.envi_len))
        game.pygame.display.set_caption(f"Make Env - {self.hole_count}")
        while self.run:
            for event in game.pygame.event.get():
                if event.type == game.pygame.QUIT:
                    self.run = False
                if event.type == game.pygame.MOUSEBUTTONDOWN:
                    cursor_pos = event.pos
                    x, y = self.get_cursor_pos(cursor_pos)
                    if self.choice == game.AGENT and not self.is_agent_placed:
                        if self.envi[y][x] > 0:
                            pass
                        else:
                            self.envi[y][x] = game.AGENT
                            self.is_agent_placed = True
                    elif self.choice == game.HOLE:
                        if self.envi[y][x] > 0:
                            pass
                        else:
                            self.envi[y][x] = game.HOLE
                            self.hole_count += 1
                    elif self.choice == game.TARGET:
                        if self.envi[y][x] > 0:
                            pass
                        else:
                            self.envi[y][x] = game.TARGET
                            self.is_treasure_placed = True
                if event.type == game.pygame.KEYDOWN:
                    if event.key == game.pygame.K_a:
                        if not self.is_agent_placed:
                            self.choice = game.AGENT
                    elif event.key == game.pygame.K_f:
                        self.choice = game.HOLE
                    elif event.key == game.pygame.K_d:
                        if not self.is_treasure_placed:
                            self.choice = game.TARGET
                    elif event.key == game.pygame.K_r:
                        self.envi = np.zeros((self.size, self.size))
                        self.hole_count = 0
                        self.is_agent_placed = False
                        self.is_treasure_placed = False
                    elif event.key == game.pygame.K_q:
                        poss = game.pygame.mouse.get_pos()
                        x, y = self.get_cursor_pos(poss)
                        if self.envi[y][x] == game.HOLE:
                            self.envi[y][x] = 0
                            self.hole_count -= 1
                        elif self.envi[y][x] == game.AGENT:
                            self.envi[y][x] = 0
                            self.is_agent_placed = False
                        elif self.envi[y][x] == game.TARGET:
                            self.envi[y][x] = 0
                            self.is_treasure_placed = False
                    elif event.key == game.pygame.K_s:
                        np.save("env", self.envi)
                        np.save("v_table", self.v_table)
                        self.run = False
            self.draw_border()
            self.draw_board()
            game.pygame.display.set_caption(f"Make Env - {self.hole_count}")
            if not self.run:
                game.pygame.image.save(self.win, game.ENV)
        game.pygame.display.quit()


class InsertAgent(Create):

    def __init__(self, envi=None, table=None, size=None):
        super().__init__(envi=envi, table=table, size=size)
        # self.envi = envi
        self.agent, _ = self.get_ag_ta()
        if not self.agent:
            self.is_agent_placed = False
        else:
            self.is_agent_placed = True
        self.choice = game.AGENT
        self.insert_agent()

    def insert_agent(self):
        game.pygame.display.set_caption("Insert Agent")
        while self.run:
            for event in game.pygame.event.get():
                if event.type == game.pygame.QUIT:
                    np.save("env", self.envi)
                    self.run = False
                if event.type == game.pygame.MOUSEBUTTONDOWN:
                    cursor_pos = event.pos
                    x, y = self.get_cursor_pos(cursor_pos)
                    if self.choice == game.AGENT:
                        if self.envi[y][x] == game.HOLE:
                            pass
                        elif self.envi[y][x] == game.AGENT:
                            self.envi[y][x] = 0
                            self.is_agent_placed = False
                        elif self.envi[y][x] == game.TARGET:
                            pass
                        else:
                            if self.is_agent_placed:
                                pass
                            else:
                                self.envi[y][x] = game.AGENT
                                self.is_agent_placed = True
                    elif self.choice == game.HOLE:
                        if self.envi[y][x] > 0 and \
                                self.envi[y][x] == game.HOLE:
                            self.envi[y][x] = 0
                        elif self.envi[y][x] > 0:
                            pass
                        else:
                            self.envi[y][x] = game.HOLE
                    elif self.choice == game.TARGET:
                        if self.envi[y][x] == game.TARGET:
                            self.envi[y][x] = 0
                        elif self.envi[y][x] > 0:
                            pass
                        else:
                            self.envi[y][x] = game.TARGET
                elif event.type == game.pygame.KEYDOWN:
                    if event.key == game.pygame.K_a:
                        if not self.is_agent_placed:
                            self.choice = game.AGENT
                    elif event.key == game.pygame.K_z:
                        self.choice = game.HOLE
                    elif event.key == game.pygame.K_d:
                        self.choice = game.TARGET
                    elif event.key == game.pygame.K_f:
                        np.save("env", self.envi)
                        self.run = False
            self.draw_border()
            self.draw_board()
            if not self.run:
                game.pygame.image.save(self.win, game.ENV)
            game.pygame.display.flip()
            self.clock.tick(self.fps)
        game.pygame.display.quit()
