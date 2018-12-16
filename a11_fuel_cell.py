import math

serial = 1309  # my puzzle input
rows = 300
cols = 300

def powerlevel(x, y, serial):
    return math.floor(((((x + 10) * y) + serial) * (x + 10)) / 100) % 10 - 5

def squareat(M, x, y):
    '''Return the sum of the 3x3 area with top-left at x,y'''
    i = y-1
    j = x-1
    answer = (M[i][j] + M[i][j+1] + M[i][j+2] +
              M[i+1][j] + M[i+1][j+1] + M[i+1][j+2] +
              M[i+2][j] + M[i+2][j+1] + M[i+2][j+2])
    return answer

def printat(M, x, y, width, height):
    x -= 1
    y -= 1
    for i in range(y, y+height):
        row = []
        for j in range(x, x+width):
            row.append(M[i][j])
        print(row)

fuelcells = [[powerlevel(j+1, i+1, serial) for j in range(0,cols)] for i in range(0,rows)]

lastmax = -float('inf')
max_coords = None
for y in range(1, rows-1):
    for x in range(1, cols-1):
        power = squareat(fuelcells, x, y)
        if power > lastmax:
            lastmax = power
            max_coords = (x, y)

print(f'Max value: {lastmax}')
print(f'Max location: {max_coords}')




