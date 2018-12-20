# TODO LIST

# GENERAL

* Write some documentation about the architecture, protocol, etc.
Consider bringing in the great draft docs from Neill's fork.


# FRET:BIT

* Remove sources of garbage collection, by recycling bytearray's
rather than repeated creating lists. This will stop the occasional
'pauses' that sometimes occur due to garbage collection coming in
at random times.

* create a 4 byte byte array tone mask and fill in lowest 8 bits.
Transmit 4 bytes-last 4 bits of the bytearray, with high bit
set on byte0 and high bit clear on bytes 1,2,3. This allows
4*7=28 fret positions to be communicated.

* Calculate our worst case tonemask buffer size (7 pads per byte)
given 5 string configurations and 8 cappo increments. Size the
tonemask buffer at both ends accordingly.

* Disable display and wire in 6 more touch pads, giving us a full 14 pads
(15 semitones with open string)

* Experiment with multiplexing the display on and off, so we can still
scan pads but still display string/capo information.

* Consider whether we want to add pad debounce to the digital inputs
that are re-purposed as touch inputs (as they sometimes bounce
a lot, as seen in the Garage-Band piano roll view).

* Add string change on button B, cycle E,A,D,G,B, and based on open string
note selected, shift all bits in tone mask up or down the buffer appropriately.
Temporarily display open string note when it changes

* Add in cappo-reset on button B when string change occurs, and
add in cappo+ on button A - so that pressing A adds 1 semitone to the range
by shifting it along the tonemask buffer by 1.
Temporarily display open string note when it changes.



# ART/MIDI:BIT

* Remove sources of garbage collection, by recycling bytearray's
rather than repeated creating lists. This will stop the occasional
'pauses' that sometimes occur due to garbage collection coming in
at random times.

* Have a 4 byte byte-array to store tone mask received from fret:bit

* cooperatively receive 1 byte at a time. If high bit set, reset
index into tonemask to position 0. If high bit clear, add one to
index up to max of len(bytearray) and ignore extra bytes. This will
allow multi-byte payloads to be sent from fret:bit and allow more fret
positions to be communicated (also paving the way for string change
and cappo at the fret:bit end)

* Remove string change mode (move over to fret:bit), but leave chord mode
on button B.

* When in chord mode display note associated with lowest set pad.
This will be the root note, and will help the musician to learn
which notes are played in which positions

* When in single mode, display note associated with highest set pad.
This will be the played note, and will help the musician to learn
which notes are played in which positions

* Consider whether there is any easy visual way to mark the selected
chord on the display. e.g. a compressed A-G that fits into 3 pixels,
and some form of 1,3,5,7,9 grouping of dots
in the right most column.

* Consider if we can add a sharp/flat tell tale dot somewhere on the
display in column 4 (row 0 for sharp, row 4 for flat, perhaps?)

* look at using other pads on the articulation hand, to trigger
bass note or melody note - meaning we don't have to keep switching
octave selector if you want to play bass and melody notes together
to introduce a simple bass-line accompanyment (bass could just use
current octave - 2 to make it lower). Two pads, so can play
just melody note, just bass note, or both.

* Look at using other pads on the articulation hand, to trigger
an up-strum or a down-strum (of the selected chord in chord mode,
or just major chord in single mode?)

* palm-mute feature, if present when plucking, create a muted sound.
If added after pluck touch, mute at that point.
