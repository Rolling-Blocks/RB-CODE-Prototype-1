from enum import Enum, auto

# Shared Enum For Project

class DispDef(Enum):
    #print(Enum.__file__)  
    # Block Actuator States
    SUBTRACT = -1
    MIDDLE = 0
    ADD = 1
    # Lock Actuator States
    LOCK = auto()
    UNLOCK = auto()
    # Block Actuators Canvas Side Location
    TOP = auto()
    BOTTOM = auto()
    # Lock Actuators Canvas Side Location
    LEFT = auto()
    RIGHT = auto()

    # Display Program
    RUN_CLOCK = auto()
    RUN_RANDIMG = auto()
    

def blockStateKey(state):
    num = -2
    if state is DispDef.SUBTRACT:
        num = -1
    if state is DispDef.MIDDLE:
        num = 0
    if state is DispDef.ADD:
        num = 1
    return num

if __name__ == '__main__':
    print(list(DispDef))
    print(blockStateKey(DispDef.SUBTRACT))
    print(blockStateKey(DispDef.MIDDLE))
    print(blockStateKey(DispDef.ADD))