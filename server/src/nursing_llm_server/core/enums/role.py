from enum import Enum, auto


class Role(Enum):
    USER = auto()
    ASSISTANT = auto()
    SYSTEM = auto()
