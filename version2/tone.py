from microbit import *
from micropython import kbd_intr

DPINS = (pin8,pin12,pin13,pin14,pin15,pin16)
PINS = (pin1,pin8,pin12,pin2,pin13,pin14,pin15,pin16)
SCAN = None
MASKS = (1,2,4,8,16,32,64,128)

def init():
    kbd_intr(-1)
    for p in PINS:
        if p in DPINS:
            p.set_pull(pin0.NO_PULL)
        else:
            p.is_touched()

def learn():
    s = [-1 for i in range(8)]
    for i in range(8):
        display.show(i)
        while True:
            m = scan(False)
            if m != 0:
                if m in MASKS:
                    b = MASKS.index(m)
                    if not (b in s):
                        s[i] = b
                        break
    return s

def scan(multi=True):
    r = 0
    for i in range(7,-1,-1):
        if SCAN is None:
            pi = i
        else:
            pi = SCAN[i]
        p = PINS[pi]
        if p in DPINS:
            v = p.read_digital() == 0
        else:
            v = p.is_touched()
        if v:
            r += MASKS[i]
            if not multi: break 
    return r

def play():
    p = 0
    tone = lambda : scan(False)
    while True:
        m = tone()
        if m != 0:
            display.show(str(MASKS.index(m)))
        else:
            display.show('-')
        if m != p:
            uart.write(bytes([m]))
            p = m

try:
    init()
    del init
    SCAN = learn()
    del learn
    display.show(Image.HAPPY)
    print(SCAN)
    sleep(250)
    
    uart.init(baudrate=115200, tx=pin0)
    play()
except Exception as e:
    display.show(Image.NO)
    uart.init(baudrate=115200)
    print(e)
    sleep(500)
finally:
    reset()
    