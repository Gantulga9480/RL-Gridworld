import pygame
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (34, 177, 76)
BLUE = (255, 0, 255)
YELLOW = (255, 255, 0)

AGENT = 11
TARGET = 22
HOLE = 99
WIDTH_MAX = 600
DRAW_VEL = 4

# 0 = up
# 1 = down
# 2 = left
# 3 = right

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


class Create:

    def __init__(self, size):
        self.floor = pygame.image.load("img\\house_down.jpg")
        self.size = size
        self.env = np.zeros((size, size))
        self.vel = WIDTH_MAX // size
        self.shape = self.vel - 1
        self.width = self.vel * self.size + 1
        self.height = self.width
        self.win = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont("arial", 40)
        self.font1 = pygame.font.SysFont("arial", 10)
        self.clock = pygame.time.Clock()
        self.choice = HOLE
        self.is_agent_placed = False
        self.is_treasure_placed = False
        self.hole_count = 0
        self.run = True
        self.fps = 60
        self.q_table = np.zeros((self.size, self.size, 4))

    def draw_board(self):
        for i in range(self.size+1):
            pygame.draw.line(self.win, WHITE, (i*self.vel, 0),
                             (i*self.vel, self.vel*self.size))
            pygame.draw.line(self.win, WHITE, (0, i*self.vel),
                             (self.vel*self.size, i*self.vel))
        for i in range(self.size):
            for j in range(self.size):
                if self.env[i][j] == AGENT:
                    pygame.draw.rect(self.win, YELLOW,
                                     (self.vel*j+1, self.vel*i+1,
                                      self.shape, self.shape))
                elif self.env[i][j] == HOLE:
                    pygame.draw.rect(self.win, RED,
                                     (self.vel*j+1, self.vel*i+1,
                                      self.shape, self.shape))
                elif self.env[i][j] == TARGET:
                    pygame.draw.rect(self.win, GREEN,
                                     (self.vel*j+1, self.vel*i+1,
                                      self.shape, self.shape))

    def draw_table(self):
        for i in range(self.size + 1):
            pygame.draw.line(self.win, BLACK, (i*self.vel, 0),
                             (i*self.vel, self.size*self.vel))
            pygame.draw.line(self.win, BLACK, (0, i*self.vel),
                             (self.size*self.vel, i*self.vel))
        for i in range(self.size):
            for j in range(self.size):
                score = self.q_table[i][j]
                string1 = f"{round(score[0], 5)} up"
                string2 = f"{round(score[1], 5)} down"
                string3 = f"{round(score[2], 5)} left"
                string4 = f"{round(score[3], 5)} right"
                s = self.font1.render(string1, 1, BLACK)
                self.win.blit(s, (j*self.vel+5, i*self.vel))
                s = self.font1.render(string2, 1, BLACK)
                self.win.blit(s, (j*self.vel+5, i*self.vel+10))
                s = self.font1.render(string3, 1, BLACK)
                self.win.blit(s, (j*self.vel+5, i*self.vel+20))
                s = self.font1.render(string4, 1, BLACK)
                self.win.blit(s, (j*self.vel+5, i*self.vel+30))

    def show_table(self):
        pygame.display.set_caption("Q_Table")
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            try:
                self.q_table = np.load("q_table.npy", allow_pickle=True)
            except IOError:
                pass
            except ValueError:
                pass
            self.win.fill(WHITE)
            self.draw_table()
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.display.quit()

    def create_env(self):
        pygame.display.set_caption("Make Env")
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cursor_pos = event.pos
                    x = int(np.floor(cursor_pos[0] / self.vel))
                    y = int(np.floor(cursor_pos[1] / self.vel))
                    if self.choice == AGENT and not self.is_agent_placed:
                        if self.env[y][x] > 0:
                            pass
                        else:
                            self.env[y][x] = AGENT
                            self.is_agent_placed = True
                    elif self.choice == HOLE:
                        if self.env[y][x] > 0:
                            pass
                        else:
                            self.env[y][x] = HOLE
                            self.hole_count += 1
                    elif self.choice == TARGET and not self.is_treasure_placed:
                        if self.env[y][x] > 0:
                            pass
                        else:
                            self.env[y][x] = TARGET
                            self.is_treasure_placed = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        if not self.is_agent_placed:
                            self.choice = AGENT
                    elif event.key == pygame.K_f:
                        self.choice = HOLE
                    elif event.key == pygame.K_d:
                        if not self.is_treasure_placed:
                            self.choice = TARGET
                    elif event.key == pygame.K_r:
                        self.env = np.zeros((self.size, self.size))
                        self.hole_count = 0
                        self.is_agent_placed = False
                        self.is_treasure_placed = False
                    elif event.key == pygame.K_q:
                        poss = pygame.mouse.get_pos()
                        x = int(np.floor(poss[0] / self.vel))
                        y = int(np.floor(poss[1] / self.vel))
                        if self.env[y][x] == HOLE:
                            self.env[y][x] = 0
                            self.hole_count -= 1
                        elif self.env[y][x] == AGENT:
                            self.env[y][x] = 0
                            self.is_agent_placed = False
                        elif self.env[y][x] == TARGET:
                            self.env[y][x] = 0
                            self.is_treasure_placed = False
                    elif event.key == pygame.K_s:
                        if self.is_agent_placed and self.is_treasure_placed \
                                and self.hole_count > 0:
                            np.save("env", self.env)
                            np.save("q_table", self.q_table)
                            self.run = False
                        else:
                            pass
            self.win.fill((0, 0, 0))
            self.draw_board()
            if not self.run:
                pygame.image.save(self.win, "img\\env_img.jpg")
            count = self.font.render(f"{self.hole_count}", 1, BLUE)
            self.win.blit(count, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.display.quit()


class Image:

    def __init__(self, shape=None, width=None, height=None):
        self.car_dim = (shape, shape)
        self.floor_dim = (width, height)

    def process(self, img_path, dim=None, save=False):
        if dim is None:
            dim = self.car_dim
        try:
            img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
            re_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
            if save:
                cv2.imwrite(img_path, re_img)
                img = pygame.image.load(img_path)
            else:
                cv2.imwrite("img\\temp.jpg", re_img)
                img = pygame.image.load("img\\temp.jpg")
                os.remove("img\\temp.jpg")
            return img
        except FileNotFoundError:
            pass

    def load_img(self):
        try:
            carImg_up = pygame.image.load("img\\down_up.png")
            carImg_right = pygame.image.load("img\\down_right.png")
            carImg_down = pygame.image.load("img\\down_down.png")
            carImg_left = pygame.image.load("img\\down_left.png")
            floor = pygame.image.load("img\\house_down.jpg")
            wall = pygame.image.load("img\\wall_down.jpg")
            star = pygame.image.load("img\\star_down.png")
        except pygame.error:
            carImg_up = cv2.imread("img\\wheel_1_up.png", cv2.IMREAD_UNCHANGED)
            carImg_right = cv2.imread("img\\wheel_1_right.png",
                                      cv2.IMREAD_UNCHANGED)
            carImg_down = cv2.imread("img\\wheel_1_down.png",
                                     cv2.IMREAD_UNCHANGED)
            carImg_left = cv2.imread("img\\wheel_1_left.png",
                                     cv2.IMREAD_UNCHANGED)
            floor = cv2.imread("img\\house.jpg", cv2.IMREAD_UNCHANGED)
            wall = cv2.imread("img\\wall.jpg", cv2.IMREAD_UNCHANGED)
            star = cv2.imread("img\\star.png", cv2.IMREAD_UNCHANGED)

            resized_up = cv2.resize(carImg_up, self.car_dim,
                                    interpolation=cv2.INTER_AREA)
            resized_right = cv2.resize(carImg_right, self.car_dim,
                                       interpolation=cv2.INTER_AREA)
            resized_down = cv2.resize(carImg_down, self.car_dim,
                                      interpolation=cv2.INTER_AREA)
            resized_left = cv2.resize(carImg_left, self.car_dim,
                                      interpolation=cv2.INTER_AREA)
            resized_floor = cv2.resize(floor, self.floor_dim,
                                       interpolation=cv2.INTER_AREA)
            resized_wall = cv2.resize(wall, self.car_dim,
                                      interpolation=cv2.INTER_AREA)
            resized_star = cv2.resize(star, self.car_dim,
                                      interpolation=cv2.INTER_AREA)

            cv2.imwrite("img\\down_up.png", resized_up)
            cv2.imwrite("img\\down_right.png", resized_right)
            cv2.imwrite("img\\down_down.png", resized_down)
            cv2.imwrite("img\\down_left.png", resized_left)
            cv2.imwrite("img\\house_down.jpg", resized_floor)
            cv2.imwrite("img\\wall_down.jpg", resized_wall)
            cv2.imwrite("img\\star_down.png", resized_star)

            carImg_up = pygame.image.load("img\\down_up.png")
            carImg_right = pygame.image.load("img\\down_right.png")
            carImg_down = pygame.image.load("img\\down_down.png")
            carImg_left = pygame.image.load("img\\down_left.png")
            floor = pygame.image.load("img\\house_down.jpg")
            wall = pygame.image.load("img\\wall_down.jpg")
            star = pygame.image.load("img\\star_down.png")
        return [carImg_up, carImg_down, carImg_left,
                carImg_right, floor, wall, star]


class GridWorld:

    def __init__(self, visual=False):
        # Game
        self.run = True
        self.game_flip = True
        self.fps = 60
        self.visual = visual
        self.clock = pygame.time.Clock()

        # Env
        try:
            self.envi = np.load("env.npy")
        except FileNotFoundError:
            self.envi = np.load("def\\env_default.npy")
        self.env_len = len(self.envi)
        self.agent, self.target = self.get_ag_ta()
        self.agent_start = self.agent
        self.env = self.get_env()
        self.vel = WIDTH_MAX // self.env_len
        self.shape = self.vel - 1
        self.width = self.vel * self.env_len + 1
        self.height = self.width
        if self.visual:
            img = Image(self.shape, self.width, self.height)
            self.images = img.load_img()
            self.carImg_up = self.images[0]
            self.carImg_down = self.images[1]
            self.carImg_left = self.images[2]
            self.carImg_right = self.images[3]
            self.floor = self.images[4]
            self.wall = self.images[5]
            self.star = self.images[6]
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"{self.env_len}x{self.env_len}")
        # Training
        try:
            self.q_table = np.load("q_table.npy")
        except FileNotFoundError:
            self.q_table = np.zeros((self.env_len, self.env_len, 4))
        self.target_reward = 2
        self.hole_reward = -2
        self.empty_step_reward = self.hole_reward / ((self.env_len - 1) * 4)

    def play(self):
        pygame.display.set_caption("GridWorld")
        while self.run:
            over = False
            state = self.reset()
            while not over:
                action = np.argmax(self.q_table[state[0]][state[1]])
                state, _, over, _, _ = self.move(action)
        pygame.display.quit()

    def show_env(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.win.fill(BLACK)
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.display.quit()

    def move(self, action):
        converged = False
        over = False
        failed = False
        reward = 0
        if self.visual:
            self.draw_game_visual(action)
        else:
            if self.game_flip:
                self.draw_game_non_visual()
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
            over = True
            reward = self.hole_reward
        elif self.agent[0] == self.target[0] and\
                self.agent[1] == self.target[1]:
            over = True
            reward = self.target_reward
        elif self.env[self.agent[0]][self.agent[1]] == 99:
            over = True
            reward = self.hole_reward
        else:
            reward = self.empty_step_reward
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                over = True
                converged = True
                failed = True
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if not self.game_flip:
                    self.game_flip = True
                elif self.game_flip:
                    self.game_flip = False
            elif keys[pygame.K_r]:
                over = True
            elif keys[pygame.K_q]:
                converged = True
                over = True
                failed = True
        return self.agent.copy(), reward, over, converged, failed

    def get_ag_ta(self):
        agent = []
        target = []
        for i in range(self.env_len):
            for j in range(self.env_len):
                if self.envi[i][j] == AGENT:
                    agent = [i, j]
                elif self.envi[i][j] == TARGET:
                    target = [i, j]
                else:
                    pass
        return agent.copy(), target.copy()

    def get_env(self):
        env = self.envi.copy()
        env[self.agent[0]][self.agent[1]] = 0
        env[self.target[0]][self.target[1]] = 0
        return env

    def reset(self):
        self.agent = self.agent_start.copy()
        return self.agent.copy()

    def draw_game_non_visual(self):
        self.win.fill(BLACK)
        for i in range(self.env_len+1):
            pygame.draw.line(self.win, WHITE, (i*self.vel, 0),
                             (i*self.vel, self.env_len*self.vel))
            pygame.draw.line(self.win, WHITE, (0, i*self.vel),
                             (self.env_len*self.vel, i*self.vel))
        for i in range(self.env_len):
            for j in range(self.env_len):
                if self.env[i][j] == HOLE:
                    pygame.draw.rect(self.win, RED,
                                     (self.vel*j+1, self.vel*i+1,
                                      self.shape, self.shape))
                else:
                    value = max(self.q_table[i][j])
                    if value > 0:
                        value *= 100
                        if value > 255:
                            value = 255
                        else:
                            pass
                        pygame.draw.rect(self.win, (0, 0, value),
                                         (self.vel*j+1, self.vel*i+1,
                                          self.shape, self.shape))
        pygame.draw.rect(self.win, GREEN,
                         (self.vel*self.target[1]+1,
                          self.vel*self.target[0]+1, self.shape, self.shape))
        pygame.draw.rect(self.win, YELLOW,
                         (self.vel*self.agent[1]+1,
                          self.vel*self.agent[0]+1, self.shape, self.shape))
        if self.game_flip:
            pygame.display.flip()
            self.clock.tick(self.fps)

    def draw_game_visual(self, dirr):
        start_pos = [self.agent[0]*self.vel+1, self.agent[1]*self.vel+1]
        for frame in range(int(self.vel/DRAW_VEL)):
            self.win.blit(self.floor, (0, 0))
            """
            for i in range(self.env_len+1):
                pygame.draw.line(self.win, WHITE, (i*self.vel, 0),
                                 (i*self.vel, self.env_len*self.vel))
                pygame.draw.line(self.win, WHITE, (0, i*self.vel),
                                 (self.env_len*self.vel, i*self.vel))
            for i in range(self.env_len):
                for j in range(self.env_len):
                    if self.env[i][j] == 99:
                        self.win.blit(self.wall, (self.vel*j+1, self.vel*i+1))
            """
            self.win.blit(self.star, (self.vel*self.target[1]+1,
                                      self.vel*self.target[0]+1))
            if dirr == UP:
                self.win.blit(self.carImg_up,
                              (start_pos[1], start_pos[0]))
                start_pos[0] -= DRAW_VEL
            elif dirr == RIGHT:
                self.win.blit(self.carImg_right,
                              (start_pos[1], start_pos[0]))
                start_pos[1] += DRAW_VEL
            elif dirr == DOWN:
                self.win.blit(self.carImg_down,
                              (start_pos[1], start_pos[0]))
                start_pos[0] += DRAW_VEL
            elif dirr == LEFT:
                self.win.blit(self.carImg_left,
                              (start_pos[1], start_pos[0]))
                start_pos[1] -= DRAW_VEL
            if self.game_flip:
                pygame.display.flip()
                self.clock.tick(self.fps)

    def draw_board(self):
        for i in range(self.env_len+1):
            pygame.draw.line(self.win, WHITE, (i*self.vel, 0),
                             (i*self.vel, self.env_len*self.vel))
            pygame.draw.line(self.win, WHITE, (0, i*self.vel),
                             (self.env_len*self.vel, i*self.vel))
        for i in range(self.env_len):
            for j in range(self.env_len):
                if self.envi[i][j] == HOLE:
                    pygame.draw.rect(self.win, RED,
                                     (self.vel*j+1, self.vel*i+1,
                                      self.shape, self.shape))
                elif self.envi[i][j] == TARGET:
                    pygame.draw.rect(self.win, GREEN,
                                     (self.vel*j+1, self.vel*i+1,
                                      self.shape, self.shape))
                elif self.envi[i][j] == AGENT:
                    pygame.draw.rect(self.win, YELLOW,
                                     (self.vel*j+1, self.vel*i+1,
                                      self.shape, self.shape))


class Training(GridWorld):

    def __init__(self, visual=True):
        super().__init__(visual=visual)
        self.epsilon = 0
        self.gamma = 0.99
        self.alpha = 0.9

    def train(self):
        self.q_table = np.zeros((self.env_len, self.env_len, 4))
        max_iter = 1000
        epsilon_min = 0
        epsilon_decay_val = (self.epsilon-epsilon_min) / (max_iter*0.9)
        episode_reward = 0
        avg_move_count = 10
        best_action = (self.env_len - 1) * 4
        converged = False
        avg_move = []
        act = 1
        show = 2
        best_action_counter = 0

        ep_reward = []
        data = {'ep': [], 'avg': [], 'min': [], 'max': [], 'eps': []}

        while not converged:
            over = False
            episode_reward = 0
            state = self.reset()
            actions = 0
            while not over:
                if np.random.random() > self.epsilon:
                    action = np.argmax(self.q_table[state[0]][state[1]])
                else:
                    action = np.random.randint(0, 3)
                new_state, reward, over, converged, failed = self.move(action)
                actions += 1
                episode_reward += reward
                if not over:
                    max_future_q_value = \
                        np.max(self.q_table[new_state[0]][new_state[1]])
                    current_q_value = self.q_table[state[0]][state[1]][action]
                    new_q_value = current_q_value+self.alpha *\
                        (reward+self.gamma*max_future_q_value-current_q_value)
                    self.q_table[state[0]][state[1]][action] = new_q_value
                elif over:
                    avg_move.append(actions)
                    self.q_table[state[0]][state[1]][action] = reward
                    if reward == self.target_reward:
                        if actions < best_action:
                            best_action_counter = 0
                            best_action = actions
                            print(f"{act} BEST episode with {best_action}")
                        elif actions == best_action:
                            print("best action repeating", best_action_counter)
                            best_action_counter += 1
                            if best_action_counter == 40:
                                converged = True
                                print("converged")
                state = new_state
            self.epsilon = max(self.epsilon - epsilon_decay_val, epsilon_min)
            ep_reward.append(episode_reward)
            if act % show == 0:
                np.save("q_table.npy", self.q_table)
            if act % show == 0:
                average_reward = \
                    sum(ep_reward[-avg_move_count:])/avg_move_count
                data['ep'].append(act)
                data['eps'].append(self.epsilon)
                data['avg'].append(average_reward)
                data['min'].append(min(ep_reward[-avg_move_count:]))
                data['max'].append(max(ep_reward[-avg_move_count:]))
            act += 1
            if self.game_flip:
                print(act, "- epsilon:", self.epsilon)
        pygame.display.quit()
        plt.plot(data['ep'], data['avg'], label="avg")
        plt.plot(data['ep'], data['eps'], label="eps")
        plt.plot(data['ep'], data['min'], label="min")
        plt.plot(data['ep'], data['max'], label="max")
        plt.legend(loc=4)
        plt.xlabel("Num_Iter")
        plt.ylabel("Reward")
        plt.title(f"learning rate={self.alpha}, discount rate={self.gamma}")
        plt.show()


class Optimize(GridWorld):

    def __init__(self, visual=False):
        super().__init__(visual=visual)
        self.state_list = []
        self.action_list = []
        self.lower = False
        self.failed = False

    def play(self):
        over = False
        self.action_list.clear()
        self.state_list.clear()
        state = self.reset()
        self.state_list.append(state)
        while not over:
            action = np.argmax(self.q_table[state[0]][state[1]])
            self.action_list.append(action)
            state, _, over, _, _ = self.move(action)
            self.state_list.append(state)

    def change_upper(self, dir_1, dir_2, s):
        if dir_2 == UP:
            if self.env[s[0]-1][s[1]] == HOLE:
                return False
            else:
                self.q_table[s[0]][s[1]][dir_2] = self.target_reward
                self.q_table[s[0]][s[1]][dir_1] = 0
                self.q_table[s[0]-1][s[1]][dir_1] = self.target_reward
                self.q_table[s[0]-1][s[1]][dir_2] = 0
                return True
        elif dir_2 == DOWN:
            if self.env[s[0]+1][s[1]] == HOLE:
                return False
            else:
                self.q_table[s[0]][s[1]][dir_2] = self.target_reward
                self.q_table[s[0]][s[1]][dir_1] = 0
                self.q_table[s[0]-1][s[1]][dir_1] = self.target_reward
                self.q_table[s[0]-1][s[1]][dir_2] = 0
                return True
        elif dir_2 == RIGHT:
            if self.env[s[0]][s[1]+1] == HOLE:
                return False
            else:
                self.q_table[s[0]][s[1]][dir_2] = self.target_reward
                self.q_table[s[0]][s[1]][dir_1] = 0
                self.q_table[s[0]][s[1]+1][dir_1] = self.target_reward
                self.q_table[s[0]][s[1]+1][dir_2] = 0
                return True
        elif dir_2 == LEFT:
            if self.env[s[0]][s[1]-1] == HOLE:
                return False
            else:
                self.q_table[s[0]][s[1]][dir_2] = self.target_reward
                self.q_table[s[0]][s[1]][dir_1] = 0
                self.q_table[s[0]][s[1]-1][dir_1] = self.target_reward
                self.q_table[s[0]][s[1]-1][dir_2] = 0
                return True

    def change_lower(self, dir_1, dir_2, s):
        if dir_2 == UP:
            if self.env[s[0]-1][s[1]] == HOLE:
                return False
            else:
                self.q_table[s[0]][s[1]][dir_2] = self.target_reward
                self.q_table[s[0]][s[1]][dir_1] = 0
                self.q_table[s[0]-1][s[1]][dir_1] = self.target_reward
                self.q_table[s[0]-1][s[1]][dir_2] = 0
                return True
        elif dir_2 == DOWN:
            if self.env[s[0]+1][s[1]] == HOLE:
                return False
            else:
                self.q_table[s[0]][s[1]][dir_2] = self.target_reward
                self.q_table[s[0]][s[1]][dir_1] = 0
                self.q_table[s[0]-1][s[1]][dir_1] = self.target_reward
                self.q_table[s[0]-1][s[1]][dir_2] = 0
                return True
        elif dir_2 == RIGHT:
            if self.env[s[0]][s[1]+1] == HOLE:
                return False
            else:
                self.q_table[s[0]][s[1]][dir_2] = self.target_reward
                self.q_table[s[0]][s[1]][dir_1] = 0
                self.q_table[s[0]][s[1]+1][dir_1] = self.target_reward
                self.q_table[s[0]][s[1]+1][dir_2] = 0
                return True
        elif dir_2 == LEFT:
            if self.env[s[0]][s[1]-1] == HOLE:
                return False
            else:
                self.q_table[s[0]][s[1]][dir_2] = self.target_reward
                self.q_table[s[0]][s[1]][dir_1] = 0
                self.q_table[s[0]][s[1]-1][dir_1] = self.target_reward
                self.q_table[s[0]][s[1]-1][dir_2] = 0
                return True

    def fix(self):
        count = 0
        for ind in range(len(self.action_list)-2):
            first = self.action_list[ind]
            second = self.action_list[ind+1]
            third = self.action_list[ind+2]
            s1 = self.state_list[ind]
            s2 = self.state_list[ind+1]
            s3 = self.state_list[ind+2]
            first_to_second_failed = False
            second_to_third_failed = False
            if first != second and second != third:
                if not self.lower:
                    self.failed = self.change_upper(second, third, s2)
                    if not self.failed:
                        pass
                    else:
                        self.lower = True
                elif self.lower:
                    self.failed = self.change_upper(first, second, s1)
                    if not self.failed:
                        pass
                    else:
                        self.lower = False
            else:
                count += 1
            continue
        return count


class Path(Optimize):

    def __init__(self, visual=False):
        super().__init__(visual=visual)
        self.play()
        self.place()
        self.show_env()

    def place(self):
        for i in range(len(self.action_list)):
            self.envi[self.state_list[i][0]][self.state_list[i][1]] = \
                self.action_list[i]+1

    def draw_board(self):
        for i in range(self.env_len+1):
            pygame.draw.line(self.win, WHITE, (i*self.vel, 0),
                             (i*self.vel, self.env_len*self.vel))
            pygame.draw.line(self.win, WHITE, (0, i*self.vel),
                             (self.env_len*self.vel, i*self.vel))
        for i in range(self.env_len):
            for j in range(self.env_len):
                if self.envi[i][j] == HOLE:
                    pygame.draw.rect(self.win, RED,
                                     (self.vel*j+1, self.vel*i+1,
                                      self.shape, self.shape))
                elif self.envi[i][j] == TARGET:
                    pygame.draw.rect(self.win, GREEN,
                                     (self.vel*j+1, self.vel*i+1,
                                      self.shape, self.shape))
                elif self.envi[i][j] == AGENT:
                    pygame.draw.rect(self.win, YELLOW,
                                     (self.vel*j+1, self.vel*i+1,
                                      self.shape, self.shape))
                elif self.envi[i][j] == UP+1:
                    pygame.draw.rect(self.win, WHITE,
                                     (self.vel*j+1, self.vel*i+1,
                                      self.shape, self.shape))
                elif self.envi[i][j] == DOWN+1:
                    pygame.draw.rect(self.win, WHITE,
                                     (self.vel*j+1, self.vel*i+1,
                                      self.shape, self.shape))
                elif self.envi[i][j] == LEFT+1:
                    pygame.draw.rect(self.win, WHITE,
                                     (self.vel*j+1, self.vel*i+1,
                                      self.shape, self.shape))
                elif self.envi[i][j] == RIGHT+1:
                    pygame.draw.rect(self.win, WHITE,
                                     (self.vel*j+1, self.vel*i+1,
                                      self.shape, self.shape))
