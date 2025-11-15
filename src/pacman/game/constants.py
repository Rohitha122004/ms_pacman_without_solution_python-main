from enum import Enum
import os

# --- Path Constants ---
# Get the directory where this constants.py file is located
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up two levels (from pacman/game -> src -> PacMan RL) and then into the 'data' folder
_DATA_ROOT = os.path.join(_BASE_DIR, 'data')


class MOVE(Enum):
    UP = "UP"
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    LEFT = "LEFT"
    NEUTRAL = "NEUTRAL"

    def opposite(self):
        opposites = {
            MOVE.UP: MOVE.DOWN,
            MOVE.RIGHT: MOVE.LEFT,
            MOVE.DOWN: MOVE.UP,
            MOVE.LEFT: MOVE.RIGHT,
            MOVE.NEUTRAL: MOVE.NEUTRAL
        }
        return opposites[self]


class GHOST(Enum):
    BLINKY = 40
    PINKY = 60
    INKY = 80
    SUE = 100

    def __init__(self, initial_lair_time):
        self.initial_lair_time = initial_lair_time


class DM(Enum):
    PATH = "PATH"
    EUCLID = "EUCLID"
    MANHATTAN = "MANHATTAN"


# Game constants
PILL = 10  # points for a normal pill
POWER_PILL = 50  # points for a power pill
# score for the first ghost eaten (doubles every time for the duration of a single power pill)
GHOST_EAT_SCORE = 200
# initial time a ghost is edible for (decreases as level number increases)
EDIBLE_TIME = 200
# reduction factor by which edible time decreases as level number increases
EDIBLE_TIME_REDUCTION = 0.9
# reduction factor by which lair times decrease as level number increases
LAIR_REDUCTION = 0.9
LEVEL_RESET_REDUCTION = 6
COMMON_LAIR_TIME = 40  # time spent in lair after being eaten
LEVEL_LIMIT = 4000  # time limit for a level
GHOST_REVERSAL = 0.0015  # probability of a global ghost reversal event
MAX_TIME = 24000  # maximum time a game can be played for
# points awarded for every life left at the end of the game (when time runs out)
AWARD_LIFE_LEFT = 800
# extra life is awarded when this many points have been collected
EXTRA_LIFE_SCORE = 10000
EAT_DISTANCE = 2  # distance in the connected graph considered close enough for an eating event to take place
NUM_GHOSTS = 4  # number of ghosts in the game
NUM_MAZES = 4  # number of different mazes in the game
DELAY = 40  # delay (in milliseconds) between game advancements
# total number of lives Ms Pac-Man has (current + NUM_LIVES-1 spares)
NUM_LIVES = 3
# difference in speed when ghosts are edible (every GHOST_SPEED_REDUCTION, a ghost remains stationary)
GHOST_SPEED_REDUCTION = 2
EDIBLE_ALERT = 30  # for display only (ghosts turning blue)
# for quicker execution: check every INTERVAL_WAIT ms to see if controllers have returned
INTERVAL_WAIT = 1

# for Competition
WAIT_LIMIT = 5000  # time limit in milliseconds for the controller to initialise
MEMORY_LIMIT = 512  # memory limit in MB for controllers (including the game)
IO_LIMIT = 10  # limit in MB on the files written by controllers

# for Maze
PATH_MAZES = "data\mazes"
PATH_DISTANCES = "data/distances"
NODE_NAMES = ["a", "b", "c", "d"]
DIST_NAMES = ["da", "db", "dc", "dd"]

# for GameView
MAG = 2
GV_WIDTH = 114
GV_HEIGHT = 130

PATH_IMAGES = "data\images"
MAZE_NAMES = ["maze-a.png", "maze-b.png", "maze-c.png", "maze-d.png"]


PATH_MAZES = os.path.join(_DATA_ROOT, 'mazes')
PATH_DISTANCES = os.path.join(_DATA_ROOT, 'distances')
PATH_IMAGES = os.path.join(_DATA_ROOT, 'images')
