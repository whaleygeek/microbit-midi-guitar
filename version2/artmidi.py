from microbit import *
from micropython import kbd_intr

octave=0
OCTAVES = [3*12,4*12,5*12]

rootidx = 0
ROOTT = "EADGB"
ROOTS = [4,9,2,7,11]
#   C C# D D# E F F# G G# A A# B
#   0 1  2 3  4 5 6  7 8  9 10 11


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

def rdtone():
    if not uart.any(): return None
    b = uart.read(1)
    return b[0]

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

    def notes_on(self, notes, velocity=None):
        if velocity is None: velocity = self.v
        if not isinstance(notes, list):
            self.send(self.NOTE_ON | self.c, notes, velocity)
        else:
            for n in notes:
                self.send(self.NOTE_ON | self.c, n, velocity)

    def notes_off(self, notes, velocity=0x7F):
        if velocity is None: velocity = self.v
        if not isinstance(notes, list):
            self.send(self.NOTE_OFF | self.c, notes, velocity)
        else:
            for n in notes:
                self.send(self.NOTE_OFF | self.c, n, velocity)

#TODO: deprecate, and use an on the fly 'notation ruler' for better range!
def newnotes():
    global NOTES
    NOTES = [n+ROOTS[rootidx]+OCTAVES[octave] for n in range(9)]

def reroot(i=None):
    global rootidx, NOTES
    if i is None:
        rootidx = (rootidx+1) % len(ROOTS)
    else:
        rootidx = i
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

def send(tm, am, chords=False):
    global playing, plucked

    if not chords:
        if tm == 0:
            notes = NOTES[0]
        else:
            for mi in range(7, -1, -1):
                if tm & MASKS[mi]:
                    tm = MASKS[mi] # highest set
                    break

            notes = NOTES[1+MASKS.index(tm)]
    else: #chord
        if tm == 0:
            notes = []
        else:
            for ri in range(8):
                if tm & MASKS[ri]:
                    break
            ri += 1 #skip open string pos
            try:
                notes = [NOTES[ri]] # root
                notes.append(NOTES[ri+4]) #3rd
                notes.append(NOTES[ri+7]) #5th
            except: pass

    pluck = (am & PLUCK) != 0
    if pluck and not plucked: # just plucked
        if playing is not None:
            midi.notes_off(playing)
        midi.notes_on(notes)
        playing = notes

    if playing is not None:
        if notes is None or notes != playing:
            midi.notes_off(playing)
            playing = None

    plucked = pluck

def play():
    pam = 0
    ptm = 0
    chords = False
    display.show(ROOTT[rootidx])
    while True:
        if button_a.was_pressed():
            reroot()
            display.show(ROOTT[rootidx])

        if button_b.was_pressed():
            chords = not chords
            if chords:
                display.show('C')
            else:
                display.show("S")

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
            send(tm, am, chords)
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
    raise e
    #print(e)
    #sleep(1000)
#finally:
    #reset()
