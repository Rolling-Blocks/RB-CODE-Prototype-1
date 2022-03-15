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

    # ACTUATION STAGES
    ROWLOCK = auto()
    COLRETURN = auto()
    ROWUNLOCK = auto()
    COLACTUATE = auto()

    # Block Actuators Canvas Side Location
    TOP = auto()
    BOTTOM = auto()
    # Lock Actuators Canvas Side Location
    LEFT = auto()
    RIGHT = auto()

    ## Image States
    IMG_NULL    = auto()
    IMG_NO      = auto()
    IMG_RAND    = auto()
    IMG_STATIC  = auto()
    ## Clock States
    CLC_NULL    = auto()
    CLC_NO      = auto()
    CLC_RUN     = auto()


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