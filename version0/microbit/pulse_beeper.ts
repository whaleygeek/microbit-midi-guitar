let item = 0
basic.forever(() => {
    if (pins.analogReadPin(AnalogPin.P1) > 512) {
        music.playTone(262, music.beat(BeatFraction.Whole))
        item += 1
        basic.showNumber(item)
        while (pins.analogReadPin(AnalogPin.P1) > 500) {

        }
    }
})
basic.showIcon(IconNames.Happy)
