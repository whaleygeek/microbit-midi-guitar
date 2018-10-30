from microbit import *

class MIDI():
    NOTE_ON  = 0x90
    NOTE_OFF = 0x80
    CHAN_MSG = 0xB0
    CHAN_BANK = 0x00
    CHAN_VOLUME = 0x07
    CHAN_PROGRAM = 0xC0
    uart.init(baudrate=115200, bits=8, parity=None, stop=1)

    @staticmethod
    def send(b0, b1, b2=None):
        if b2 is None: m = bytes([b0,b1])
        else: m = bytes([b0,b1,b2])
        uart.write(m)

    def __init__(self, channel=0, velocity=0x7F):
        self.channel = channel
        self.velocity = velocity
        
    def set_instrument(self, instrument):
        instrument -= 1
        if instrument<0 or instrument>0x7F: return
        self.send(self.CHAN_PROGRAM|self.channel, instrument)

    def note_on(self, note, velocity=None):
        if note<0 or note>0x7F:return
        if velocity is None: velocity=self.velocity
        if velocity<0 or velocity>0x7F: velocity=0x7F
        self.send(self.NOTE_ON|self.channel, note, velocity)

    def note_off(self, note, velocity=0x7F):
        if note<0 or note>0x7F:return
        if velocity is None: velocity=self.velocity
        if velocity<0 or velocity>0x7F: velocity=0x7F
        self.send(self.NOTE_OFF|self.channel, note, velocity)

midi = MIDI()
display.show('-')

#pin0=plucka, pin1=pluckb, pin2=mute, PINS=scale notes
PINS = [pin8, pin12, pin13, pin14, pin15, pin16]
O=5
#C D E F G A B
SCALE = [0,2,4,5,7,9,11]
NOTES = [n+(O*12) for n in SCALE]
#mutes = [-1 for i in range(7)]

for pin in PINS:
    pin.set_pull(pin0.NO_PULL)

def get_highest():
    for p in range(len(PINS)-1, -1, -1):
        if PINS[p].read_digital() == 0: # touch pulls down
            return p
    return None
     
def tester():
    display.clear()
    for p in range(len(PINS)):
        if not PINS[p].read_digital(): # low is active
            y = int(p / 5)
            x = p % 5
            display.set_pixel(x,y,9)
    
note = None
plucked = False

while True:
    pluck = pin0.is_touched()
    if pluck and not plucked:
        if note is not None:
            midi.note_off(note)
            note = None
        ni = get_highest()
        if ni is not None:
            display.show(ni)
            note = NOTES[ni]
            midi.note_on(note)

    elif not pluck and plucked:
        if note is not None:
            midi.note_off(note)
            note = None

    plucked = pluck
    


