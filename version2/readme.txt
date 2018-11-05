TODO

- add fingering dictionary for our 15 supported chords
- add chord dictionary for our supported chords
- detect fingerings and convert into chord notes then play

Position of lowest fretted note sets the root
(so root is always present)

Chords chosen:

NAME    FINGERING   binary      positions in tetra-chord
--------------------------------------------------------
Root    . - - - -   0           1
MAJ     . . . - -   12          1  3  5
MAJ7    . . . . -   14          1  3  5  7
7       . - - . -   2           1  3  5  b7
min     . - . - -   4           1  b3 5
min7    . - . . -   6           1  b3 5  b7
min9    . - . - .   5           1  b3 5  b7 9
5       . . - - -   8           1     5
5/9     . . - - .   9           1  5        9
6       . - . . .   7           1  3  5  6
9       . . . - .   13          1  3  5  b7 9
aug     . . - . -   10          1  3  #5
sus4    . - - - .   1           1  4  5
7sus4   . - - . .   3           1  4  5  b7
dim     . . - . .   11          1  b3 b5 bb7

And, for aliens with 5 fingers and a thumb...
mental  . . . . .   15

- decide on octave positions based on strings
(might make it more like a guitar)