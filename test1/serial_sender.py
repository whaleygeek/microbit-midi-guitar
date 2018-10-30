from microbit import *

uart.init(baudrate=115200, tx=pin0)
display.show("s")
timeout = None

while True:
    if button_a.was_pressed():
        display.show("A")
        timeout = running_time() + 1000
        uart.write("A")

    elif button_b.was_pressed():
        display.show("B")
        timeout = running_time() + 1000
        uart.write("B")

    if timeout is not None and running_time() > timeout:
        timeout = None
        display.show("s")
