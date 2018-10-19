basic.forever(() => {
    if (pins.analogReadPin(AnalogPin.P0) > 512) {
        led.plot(2, 2)
        radio.sendString("PLUCK")
        while (pins.analogReadPin(AnalogPin.P0) > 500) {

        }
        led.unplot(2, 2)
    }
})
radio.setGroup(0)
basic.showIcon(IconNames.Square)