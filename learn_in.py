# learn up to 8 touch input positions

from microbit import *

DPINS = (pin8,pin12,pin13,pin14,pin15,pin16)
PINS = (pin1,pin8,pin12,pin2,pin13,pin14,pin15,pin16)
MAPPING = None
MASKS = (1,2,4,8,16,32,64,128)

def init():
    for p in PINS:
        if p in DPINS:
            p.set_pull(pin0.NO_PULL)
        else:
            p.is_touched()

def learn():
    mapping = []
    for i in range(8):
        display.show(i+1)
        while True:
            t = scan(False)
            if t != 0 and t not in mapping:
                mapping.append(t)
                break
    return mapping

def scan(multi=True):
    r = 0
    for i in range(8):
        p = PINS[i]
        if p in DPINS:
            v = p.read_digital() == 0
        else:
            v = p.is_touched()
        if v:
            m = MASKS[i]
            if MAPPING is None:
                r += m
            else:
                r += MASKS[MAPPING.index(m)]
            if not multi: break 
    return r

def play():
    while True:
        t = scan(False)
        if t != 0:
            display.show(str(MASKS.index(t)))
        else:
            display.show('?')

init()
del init
MAPPING = learn()
del learn
display.show(Image.HAPPY)

sleep(500)
play()

