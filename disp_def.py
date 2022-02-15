from enum import Enum, auto

# Shared Enum For Project

class DispDef(Enum):
    #print(Enum.__file__)  
    # Block Actuator States
    ADD = 1
    MIDDLE = 0
    SUBTRACT = -1
    # Lock Actuator States
    LOCK = auto()
    UNLOCK = auto()
    # Block Actuators Canvas Side Location
    TOP = auto()
    BOTTOM = auto()
    # Lock Actuators Canvas Side Location
    LEFT = auto()
    RIGHT = auto()

if __name__ == '__main__':
    print(list(DispDef))
