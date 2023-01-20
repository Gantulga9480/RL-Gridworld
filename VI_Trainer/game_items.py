# Game control
AGENT = 11
TARGET = 22
HOLE = 99

STEP_REWARD = 0
TARGET_REWARD = 0
OUT_REWARD = -2

GAMMA = 0.9

TRANSITIONS = [1, 1, 1, 1]

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

FPS = 60

# Game visual
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (34, 255, 76)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

WIDTH_MAX = 600
DRAW_VEL = 4

WHEEL_UP = r"img\raw\wheel_u.png"
WHEEL_RIGHT = r"img\raw\wheel_r.png"
WHEEL_DOWN = r"img\raw\wheel_d.png"
WHEEL_LEFT = r"img\raw\wheel_l.png"

WHEEL_UP_RE = r"img\re\wheel_u_r.png"
WHEEL_RIGHT_RE = r"img\re\wheel_r_r.png"
WHEEL_DOWN_RE = r"img\re\wheel_d_r.png"
WHEEL_LEFT_RE = r"img\re\wheel_l_r.png"

FLOOR = r"img\raw\floor.jpg"
GRASS = r"img\raw\grass.jpg"
HOUSE = r"img\raw\house.jpg"
STAR = r"img\raw\star.png"
WALL = r"img\raw\wall.jpg"

FLOOR_RE = r"img\re\floor_r.jpg"
GRASS_RE = r"img\re\grass_r.jpg"
HOUSE_RE = r"img\re\house.jpg"
STAR_RE = r"img\re\star_r.png"
WALL_RE = r"img\re\wall_r.jpg"

DEFAULT_ENV = r"def\default_env_img.jpg"
ENV = r"img\re\env_img.jpg"

# Custom Exceptions


class NoAgent(Exception):
    """Raised when no agent placed in env file"""
    pass
