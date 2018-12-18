# frets.py - left handed fretboard scanner

from microbit import *

DPINS = (pin8,pin12,pin13,pin14,pin15,pin16)
PINS = (pin1,pin8,pin12,pin2,pin13,pin14,pin15,pin16)

def init():
    for p in PINS:
        if p in DPINS:
            p.set_pull(pin0.NO_PULL)
        else:
            p.is_touched()

def scan():
    r = 0
    for i in range(len(PINS)):
        p = PINS[i]
        if p in DPINS:
            v = p.read_digital() == 0
        else:
            v = p.is_touched()
        if v:
            r += 1<<i
    return r

def play():
    ptm = 0
    while True:
        tm = scan()
        if tm != 0:
            #TODO: can we display note?
            #we will know string/cappo
            #but won't know if in chord or single mode
            #chord mode uses lowest pad for root
            #single mode uses highest pad for fretted
            display.show(Image.DIAMOND)
        else:
            display.show('-')
        #TODO: shift tm by cappo/string offset
        if tm != ptm:
            #TODO: send multi bytes with first bit set for start of frame
            #which allows any number of bytes in a frame without a len byte
            #but 7 bits per byte, with safe receiver re-sync at start.
            #TODO recycle object rather than use and forget for garbage
            #Need to prevent all garbage collection if possible
            #use a fixed bytearray, it is assignable.
            #check uart.write accepts it as supporting bytes interface.
            uart.write(bytes([tm]))
            ptm = tm

try:
    init()
    del init
    display.show(Image.HAPPY)
    sleep(250)
    uart.init(baudrate=115200, tx=pin0)
    play()
except Exception as e:
    display.show(Image.NO)
    sleep(1000)
finally:
    reset()
