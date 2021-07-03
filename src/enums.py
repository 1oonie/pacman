import enum


class Enum(enum.Enum):
    def __repr__(self) -> str:
        return "<{0}>".format(self._name_)


class Tile(Enum):
    BLANK = 0
    COIN = 1
    WALL = 2
    POWER_PELLET = 3


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 3
    DOWN = 4
    NONE = 5

class GhostMode(Enum):
    CHASE = 0
    SCATTER = 1
