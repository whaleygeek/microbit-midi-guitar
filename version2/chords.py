# chords.py - 05/11/2018  D.J.Whale
#
# Used to generate a compressed version of the chord table
# (to save MicroPython memory, as it stays fixed)

# A Tetra-Chord has intervals: tone, tone, semitone.
# Concatenate two Tetra-Chords with a bridge tone to get the major scale
# tone, tone, semitone, bridge-tone, tone, tone, semitone
# (additionally, use chromatic names when vocalising,
# so if you have 'D D#' then spell it 'D Eb' so each letter is used once.

# This is a semitone notation ruler, inspired by Candida Tobin's
# work with The Tobin Music Method.
# This notation-ruler has two complete scales concatenated.
# It is used to measure note distances.
# Each tuple index is the position (1st, 2nd, 3rd, etc)
# Each value is the number of semi-tones away from its root, of that position.

#    (0)    R 2 3 4 5 6 7  8  9  10 11 12 13 14 15
NR = (None, 0,2,4,5,7,9,11,12,14,16,17,19,21,23,24)


# Note fingerings are rooted at the lowest touched pad.
# This design is partly inspired by the Guitar Zeros, who used 5 pads
# on a Playstation Guitar Hero controller to finger lots of chords
# using binary patterns on the 5 buttons. However, our approach is moveable
# along the fretboard as we have more touch pads.
#
# The 4 pads to right of root create a pattern that is visually logical
# (for most of the common chords) to aid remembering them.
# If you think of the columns from left to right as 1st 3rd 5th 7th 9th,
# it mostly makes visual sense. There is always a root note fingered,
# as this places the chord position.
#
# The chords chosen for inclusion were selected based on looking at a
# guitar pocket chord book, and also comparing against a number of pop songs
# that we'd like to learn to play. It is not exhaustive.
#
# This design table is ordered in logical order in the hope that it bettr
# conveys the logical design patterns of the fingering. In the actual
# chord table, the fingerings are stored in binary order so that the table
# can use a computed index for a fast lookup.

#NAME    FINGERING   binary  positions        pattern logic
#-------------------------------------------------------------------------------
# Root    . - - - -   0       1               just the root note plays
# MAJ     . . . - -   12      1  3  5         first 3 cols look like 1,3,5
# MAJ7    . . . . -   14      1  3  5  7      MAJ +7th
# 7       . - - . -   2       1  3  5  b7     Root +7th
# min     . - . - -   4       1  b3 5         MAJ with adjusted 3rd
# min7    . - . . -   6       1  b3 5  b7     min +7th
# min9    . - . - .   5       1  b3 5  b7 9   min +9th
# 5       . . - - -   8       1     5         looks like a power chord on guitar
# 5/9     . . - - .   9       1  5        9   looks like a power chord on guitar
# 6       . - . . .   7       1  3  5  6      (no logic)
# 9       . . . - .   13      1  3  5  b7 9   MAJ +9th
# aug     . . - . -   10      1  3  #5        MAJ with 5th raised
# sus4    . - - - .   1       1  4  5         (no logic)
# 7sus4   . - - . .   3       1  4  5  b7     sus4 +7th
# dim     . . - . .   11      1  b3 b5 bb7    (no logic) just hard to finger!
#
# And, for aliens with 5 fingers and a thumb, there is potentially a chord 15
# which is impossible for humans to play, as the thumb forms the ground plane
# on the back of the guitar neck.
# mental  . . . . .   15


CHORDS = (
    (NR[1],),                                    # 0   root  . - - - -
    (NR[1], NR[4],   NR[5]),                     # 1   sus4  . - - - .
    (NR[1], NR[3],   NR[5],   NR[7]-1),          # 2   7     . - - . -
    (NR[1], NR[4],   NR[5],   NR[7]-1),          # 3   7sus4 . - - . .
    (NR[1], NR[3]-1, NR[5]),                     # 4   min   . - . - -
    (NR[1], NR[3]-1, NR[5],   NR[7]-1,  NR[9]),  # 5   min9  . - . - .
    (NR[1], NR[3]-1, NR[5],   NR[7]-1),          # 6   min7  . - . . -
    (NR[1], NR[3],   NR[5],   NR[6]),            # 7   6     . - . . .
    (NR[1],          NR[5]),                     # 8   5     . . - - -
    (NR[1], NR[5],                      NR[9]),  # 9   5/9   . . - - .
    (NR[1], NR[3],   NR[5]+1),                   # 10  aug   . . - . -
    (NR[1], NR[3]-1, NR[5]-1, NR[7]-2),          # 11  dim   . . - . .
    (NR[1], NR[3],   NR[5]),                     # 12  MAJ   . . . - -
    (NR[1], NR[3],   NR[5],   NR[7]-1,  NR[9]),  # 13  9     . . . - .
    (NR[1], NR[3],   NR[5],   NR[7]),            # 14  MAJ7  . . . . -
)

# This generates a tuple of tuples (immutable) with semitone offsets from root
# of the specific note. It can be embedded inside a MicroPython code file
# and used to spell out chords from any root.

print("CHORDS = %s" % str(CHORDS))


