from enum import IntEnum, Enum

class AppCode(IntEnum):
    QUIT = 0
    EXIT = 1
    START = 2
    OK = 3
    UNHANDLED = 4

class State(IntEnum):
    START = 0
    RUNNING = 1
    PAUSE = 2
    GAMEOVER = 255

class DrawCode(Enum):
    NORMAL = "exact"
    CENTER = "center"
