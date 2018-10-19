from microbit import *
import radio

def print(*args, **kwargs):
    pass # disable print, now UART is in use
    
class MIDI():
    NOTE_ON  = 0x90
    NOTE_OFF = 0x80
    CHAN_MSG = 0xB0
    CHAN_BANK = 0x00
    CHAN_VOLUME = 0x07
    CHAN_PROGRAM = 0xC0

    uart.init(baudrate=31250, bits=8, parity=None, stop=1, tx=pin0)

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

def get_message():
    while True:
        try:
            msg = radio.receive_bytes()
            if msg is not None:
                if len(msg) >= 13 and msg[3] == 2:
                    lstr = msg[12] # length byte
                    text = str(msg[13:13+lstr], 'ascii')
                    return text
            else:
                return None
                
        except Exception as e: # reset radio on error
            radio.off()
            radio.on()            

midi = MIDI()

radio.config(channel=7, address=0x75626974, group=0, data_rate=radio.RATE_1MBIT)
radio.on()
display.show(Image.DIAMOND_SMALL)

def get_note():
    middle_c = 60 # C4
    x = accelerometer.get_x()
    x = min(x, 1000)
    x = max(x, -1000)
    x = int(x / 42)
    note = x + middle_c
    return note

hold = None

while True:

    note = get_note()

    if button_a.was_pressed():
        display.show(Image.DIAMOND)
        midi.note_on(note)
        sleep(50)
        midi.note_off(note)
        display.show(Image.DIAMOND_SMALL)

    elif button_b.is_pressed():
        if not hold:
            hold = note
            midi.note_on(note)
    else:
        if hold:
            midi.note_off(hold)
            hold = None
            
        msg = get_message()
        if msg is not None:
            display.show(Image.DIAMOND)
            midi.note_on(note)
            sleep(50)
            midi.note_off(note)
            display.show(Image.DIAMOND_SMALL)
