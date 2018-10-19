# mb-guitar
An electric guitar, made from a micro:bit

# arduino code

There is a little bit of arduino code here for the ATTiny85.
It is basically a configurable pulse stretcher. The impulse from the piezo
hit is quite short in practice, and without a high speed trigger interrupt
enabled by default on the micro:bit, it's easy to miss the piezo pulse.

PB0 is the trigger in from the piezo (which is protected by a 3V3 zenner
to prevent over voltage, a 1N4148 to prevent under voltage, and a 1M
resistor to prevent any residual charge building up on the piezo).

PB4 is the HOLD output, and it is configured to generate a 50ms pulse.

I spent a happy evening brushing up my electronics skills, building a 
two-transistor monostable that acted as a pulse stretcher. I then
discovered that I needed a really high impedance input in order to be
able to sense the voltage spike from the piezo. After a bit of time
exerimenting with 741 opamps, then remembering they need at least 4.5V
for the supply rail (and I'll be running all of this off of 3V for the
micro:bit), I decided it would be much easier to use the ATTiny85 chip.

This is mostly because the input pins are a high impedence, but also
if you work it out, the cost and component count using the ATTiny85
is much lower in both cases, and it is also much easier to construct.


