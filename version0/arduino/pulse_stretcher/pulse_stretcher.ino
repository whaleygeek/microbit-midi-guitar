/* pulse_stretcher.ino  (c) 14/05/2017  D.J.Whale
 *
 * Stretch a tiny input pulse from a piezo sensor into a longer pulse.
 * This is so that an unmodified micro:bit can sense a 'hit' on a piezo
 * thus using it as an input device.
 */

#define TRIGGER   0 // PB0
#define HOLD      4 // PB4
#define ONTIME_MS 50

void setup() 
{                
    pinMode(TRIGGER, INPUT);
    pinMode(HOLD, OUTPUT);
    digitalWrite(HOLD, LOW);
}

void loop()
{
    //NOTE: no glitch filtering
    if (digitalRead(TRIGGER)) 
    {
        digitalWrite(HOLD, HIGH);
        delay(ONTIME_MS);

        // wait for input to go low before resetting
        while (digitalRead(TRIGGER))
        {
            // wait
        }

        digitalWrite(HOLD, LOW);
    }
}


