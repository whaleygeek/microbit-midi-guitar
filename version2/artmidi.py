from microbit import *
from micropython import kbd_intr

octave=0
OCTAVES = [3*12,4*12,5*12]

rootidx = 0
ROOTT = "EADGB"
ROOTS = [4,9,2,7,11]
#   C C# D D# E F F# G G# A A# B
#   0 1  2 3  4 5 6  7 8  9 10 11

fingering = 0
FINGERT = "SMP"
FINGERINGS = [
    [0,1,2,3,4,5,6,7,8], #sem
    [0,2,4,5,7,9,11,12,14], #maj
    [1,3,6,8,10, 13,15,18,20] #pent
]

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

def rdart():
    r = 0
    for i in range(7,-1,-1):
        p = PINS[i]
        if p in DPINS:
            v = p.read_digital() == 0
        else:
            v = p.is_touched()
        if v:
            r += MASKS[i]
    return r

def rdtone(multi=False):
    if not uart.any(): return None
    b = uart.read(1)
    ##if b is None: return None
    tm = b[0]
    if not multi:
        for mi in range(7,-1,-1):
            if tm & MASKS[mi]:
                return MASKS[mi]
    return tm

class MIDI():
    NOTE_ON = 0x90
    NOTE_OFF = 0x80

    @staticmethod
    def send(b0, b1, b2=None):
        if b2 is None:
            m = bytes([b0, b1])
        else:
            m = bytes([b0, b1, b2])
        uart.write(m)

    def __init__(self, c=0, v=0x7F):
        self.c = c
        self.v = v

    def note_on(self, note, velocity=None):
        if velocity is None: velocity = self.v
        self.send(self.NOTE_ON | self.c, note, velocity)

    def note_off(self, note, velocity=0x7F):
        if velocity is None: velocity = self.v
        self.send(self.NOTE_OFF | self.c, note, velocity)

def newnotes():
    global NOTES
    NOTES = [n+ROOTS[rootidx]+OCTAVES[octave] for n in FINGERINGS[fingering]]

def reroot(i=None):
    global rootidx, NOTES
    if i is None:
        rootidx = (rootidx+1) % len(ROOTS)
    else:
        rootidx = i
    newnotes()

def refinger(i=None):
    global fingering
    if i is None:
        fingering = (fingering+1) % len(FINGERINGS)
    else:
        fingering = i
    newnotes()

def reoctave(i=None):
    global octave
    if i is None:
        octave = (octave+1) % len(OCTAVES)
    else:
        octave = i
    newnotes()

midi = MIDI()

playing = None
plucked = False
PLUCK = 1<<5
LOW=1<<4
MID=1<<3
HIGH=1<<2

newnotes()

def send(tm, am):
    global playing, plucked

    pluck = (am & PLUCK) != 0
    if tm == 0: note = NOTES[0]
    else: note = NOTES[1+MASKS.index(tm)] #tm=single

    if pluck and not plucked: # just plucked
        if playing is not None:
            midi.note_off(playing)
        midi.note_on(note)
        playing = note

    if playing is not None:
        if note is None or note != playing:
            midi.note_off(playing)
            playing = None

    plucked = pluck

def play():
    pam = 0
    ptm = 0
    display.show(ROOTT[rootidx])
    while True:
        if button_a.was_pressed():
            reroot()
            display.show(ROOTT[rootidx])

        if button_b.was_pressed():
            refinger()
            display.show(FINGERT[fingering])
            sleep(500)
            display.show(ROOTT[rootidx])

        tm = rdtone()
        if tm is None: tm = ptm
        am = rdart()

        if (am & LOW) != 0:
            reoctave(0)
        elif (am & MID) != 0:
            reoctave(1)
        elif (am & HIGH) != 0:
            reoctave(2)

        if am != pam or tm != ptm:
            send(tm, am)
            pam = am
            ptm = tm

try:
    init()
    del init
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
