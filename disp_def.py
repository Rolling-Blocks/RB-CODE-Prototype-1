from enum import Enum, auto
#
# Shared Enum For Project

class DispDef(Enum):
    #print(Enum.__file__)  
    
    # Servo_Types
    LOCK_SERVO = auto()
    BLOCK_SERVO = auto()

    # Block Actuator States
    SUBTRACT    = -1
    MIDDLE      =  0
    ADD         =  1

    # Lock Actuator States
    LOCK        = auto()
    UNLOCK      = auto()

    # ACTUATION STAGES
    ROWLOCK     = auto()
    COLRETURN   = auto()
    ROWUNLOCK   = auto()
    COLACTUATE  = auto()

    ## Actuators Canvas Side Location
        ## Block
    TOP         = auto()
    BOTTOM      = auto()
        ## Lock 
    LEFT        = auto()
    RIGHT       = auto()

    ## States
        ## Image
    IMG_NULL    = auto()
    IMG_NO      = auto()
    IMG_RAND    = auto()
    IMG_STATIC  = auto()
        ## Clock
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