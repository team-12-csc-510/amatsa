from enum import Enum, auto


class AlarmType(Enum):
    DISK = auto()
    SYSTEM = auto()


class AlarmThreshold(Enum):
    DISK = 80
    SYSTEM = 90
