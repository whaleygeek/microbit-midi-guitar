from microbit import *

uart.write("START\n")
uart.init(baudrate=115200, rx=pin0)
display.show("b")

timeout = None

while True:
    rx = uart.read()
    if rx is not None:
        uart.write(rx)
        display.show(Image.DIAMOND)
        timeout = running_time() + 1000
            
    if timeout is not None and running_time() > timeout:
        timeout = None
        display.show("b")
        
