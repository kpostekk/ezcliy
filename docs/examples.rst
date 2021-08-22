Examples
============

Basic sqaure root
------------------
.. literalinclude:: _static/example_1.py

Example calls
**************

>>> python3 example.py 2
4

>>> python3 example.py 4
16

>>> python3 example.py --help
Usage: example [the number to be squared] [PARAMETERS]
Positionals:
    the number to be squared -> should be an int
Flags:
    --help -> Shows help.

Small cli calculator
---------------------
.. literalinclude:: _static/example_2.py

>>> python3 qmath.py
Usage: qmath.py [VALUES...] [COMMANDS] [PARAMETERS]
Commands:
    sum -> Sums all passed values.
    product -> Product of all passed values.
    root
Flags:
    --help -> Shows help even when no arguments are passed.
    -f --floor
    -c --ceil

>>> python3 qmath.py sum --help
Usage: sum [VALUES...] [PARAMETERS]
Description:
    Sums all passed values.
Flags:
    --help -> Shows help even when no arguments are passed.
    -f --floor
    -c --ceil

>>> python3 qmath.py sum 9 21 90 11.9
131.9

>>> python3 qmath.py sum 0.4 0.5 -c
1

>>> python3 qmath.py sum 0.4 0.5 --floor
0

>>> python3 qmath.py root 4 0.5
8.0
