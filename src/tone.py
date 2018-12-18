from microbit import *

DPINS = (pin8,pin12,pin13,pin14,pin15,pin16)
PINS = (pin1,pin8,pin12,pin2,pin13,pin14,pin15,pin16)
SCAN = None
MASKS = (1,2,4,8,16,32,64,128)

def init():
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

def rdtone():
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
    return r

def play():
    ptm = 0
    while True:
        tm = rdtone()
        if tm != 0:
            display.show(Image.DIAMOND)
        else:
            display.show('-')
        if tm != ptm:
            uart.write(bytes([tm]))
            ptm = tm

try:
    init()
    del init
    if button_a.is_pressed():
        SCAN = learn()
        del learn
        print(SCAN)
    display.show(Image.HAPPY)
    sleep(250)
    uart.init(baudrate=115200, tx=pin0)
    play()
except Exception as e:
    display.show(Image.NO)
    uart.init(baudrate=115200)
    print(e)
    sleep(1000)
finally:
    reset()
