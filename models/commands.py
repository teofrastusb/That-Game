from enum import Enum, auto
class Commands(Enum):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    BITE = auto()
    BITELEFT = auto()
    BITERIGHT = auto()
    BITEUP = auto()
    BITEDOWN = auto()
    SPLIT = auto()
    MERGE = auto()

    def is_move(self):
        return self in (Commands.LEFT, Commands.RIGHT, Commands.UP, Commands.DOWN)

    def is_bite(self):
        return self in (Commands.BITE, Commands.BITELEFT, Commands.BITERIGHT, Commands.BITEUP, Commands.BITEDOWN)