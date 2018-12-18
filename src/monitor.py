from microbit import *
from micropython import kbd_intr

kbd_intr(-1)
uart.init(baudrate=115200, rx=pin0)

while True:
    if uart.any():
        b = uart.read(1)
        b = b[0]
        display.show(str(b))
        sleep(250)
    else:
        display.show(Image.DIAMOND)


