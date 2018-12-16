# This is a rewrite of my original (slower) answer 
# now using a summed-area table.
# https://en.wikipedia.org/wiki/Summed-area_table

import math
from collections import defaultdict 

serial = 1309  # my puzzle input
cell_size = 300

def powerlevel(x, y, serial=serial):
    return math.floor(((((x + 10) * y) + serial) * (x + 10)) / 100) % 10 - 5

def create_summedareatable(rows, cols):
    I = defaultdict(int)
    for y in range(1,rows+1):
        for x in range(1,cols+1):
            I[(x,y)] = I[(x-1,y)] + I[(x,y-1)] -I[(x-1,y-1)] + powerlevel(x,y)
    return I

def squareat(A, x, y, size):
    '''Return the sum of the size x size area with top-left at x,y'''
    return (A[(x+size-1, y+size-1)]
            - A[(x-1, y+size-1)]
            - A[(x+size-1, y-1)]
            + A[(x-1, y-1)])

A = create_summedareatable(cell_size, cell_size)

lastmax = -float('inf')
max_coords = None
for size in range(1, cell_size+1):
    # print(size, lastmax, max_coords)
    for y in range(1, cell_size+1-size-1):
        for x in range(1, cell_size+1-size-1):
            power = squareat(A, x, y, size)
            if power > lastmax:
                lastmax = power
                max_coords = (x, y, size)

print(f'Max value: {lastmax}')
print(f'Max location (x, y, size): {max_coords}')



