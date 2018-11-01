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

rdart = lambda: scan(True)

def rdtone():
    tm = None
    if uart.any():
        b = uart.read(1)
        if b is not None:
            tm = b[0]
    return tm


class MIDI():
    NOTE_ON = 0x90
    NOTE_OFF = 0x80
    #CHAN_MSG = 0xB0
    #CHAN_BANK = 0x00
    #CHAN_VOLUME = 0x07
    CHAN_PROGRAM = 0xC0

    @staticmethod
    def send(b0, b1, b2=None):
        if b2 is None:
            m = bytes([b0, b1])
        else:
            m = bytes([b0, b1, b2])
        uart.write(m)

    def __init__(self, channel=0, velocity=0x7F):
        self.channel = channel
        self.velocity = velocity

    def set_instrument(self, instrument):
        instrument -= 1
        if instrument < 0 or instrument > 0x7F: return
        self.send(self.CHAN_PROGRAM | self.channel, instrument)

    def note_on(self, note, velocity=None):
        if note < 0 or note > 0x7F: return
        if velocity is None: velocity = self.velocity
        if velocity < 0 or velocity > 0x7F: velocity = 0x7F
        self.send(self.NOTE_ON | self.channel, note, velocity)

    def note_off(self, note, velocity=0x7F):
        if note < 0 or note > 0x7F: return
        if velocity is None: velocity = self.velocity
        if velocity < 0 or velocity > 0x7F: velocity = 0x7F
        self.send(self.NOTE_OFF | self.channel, note, velocity)

midi = MIDI()
O=5
#(C) D E F G A B C D
SCALE = [0,2,4,5,7,9,11,12,14]
NOTES = [n+(O*12) for n in SCALE]
playing = None
plucked = False
PLUCK = 1<<5

def send(tm, am):
    global playing, plucked

    pluck = (am & PLUCK) != 0
    if tm == 0: note = NOTES[0]
    else: note = NOTES[1+MASKS.index(tm)] #tm=single

    if pluck:
        if not plucked:
            if playing is not None:
                print("OFF:%d" % playing)
                playing = None
            print("ON:%d" % note)
            playing = note

        else: # plucked
            if note != playing:
                print("OFF:%d" % playing)
                print("ON:%d" % note)
                playing = note

    else: #not pluck
        pass # leave note sustained

    plucked = pluck

def play():
    pam = 0
    ptm = 0
    while True:
        tm = rdtone()
        if tm is None: tm = ptm

        am = rdart()
        if am != 0:
            try:
                display.show(str(MASKS.index(am)))
            except: # probably multi
                display.show(Image.DIAMOND)
        else:
            display.show('-')

        if am != pam or tm != ptm:
            send(tm, am)
            pam = am
            ptm = tm

try:
    print("ART/MIDI")
    init()
    del init
    if button_a.is_pressed():
        SCAN = learn()
        del learn
        print(SCAN)
    display.show(Image.HAPPY)
    sleep(250)
    
    uart.init(baudrate=115200, rx=pin0)
    play()
except Exception as e:
    display.show(Image.NO)
    uart.init(baudrate=115200)
    print(e)
    sleep(1000)
finally:
    reset()
