import random
import os
import time

FORMS = [
    [[
        '.....',
        '.....',
        '.....',
        '0000.',
        '.....'
    ],
    [
        '.....',
        '..0..',
        '..0..',
        '..0..',
        '..0..'
    ]],[[
        '.....',
        '.....',
        '..0..',
        '.000.',
        '.....'
    ],[
        '.....',
        '..0..',
        '.00..',
        '..0..',
        '.....'
    ],[
        '.....',
        '.....',
        '.000.',
        '..0..',
        '.....'
    ], [
        '.....',
        '..0..',
        '..00.',
        '..0..',
        '.....'
    ]],
]

COLORS = ['red', 'green', 'blue','yellow']

GRID_SIZE = 10

WIDTH = GRID_SIZE * 10
HEIGHT = GRID_SIZE * 20
