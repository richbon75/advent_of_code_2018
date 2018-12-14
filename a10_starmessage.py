
# stars will be a list of tuples
stars = []
velocities = []
with open('a10_input.txt', 'r') as f:
    for line in f:
        x = int(line[line.index('<')+1:line.index(',')])
        y = int(line[line.index(',')+1:line.index('>')])
        line = line[line.index('>')+1:]
        dx = int(line[line.index('<')+1:line.index(',')])
        dy = int(line[line.index(',')+1:line.index('>')])
        stars.append((x, y))
        velocities.append((dx, dy))

def positions(stars, velocities, seconds):
    # return a list of (x,y) tuples representing the stars'
    # postions after a particular number of seconds
    updatedpositions = list()
    for i in range(0, len(stars)):
        s = stars[i]
        v = velocities[i]
        updatedpositions.append((s[0] + v[0] * seconds, s[1] + v[1] * seconds))
    return updatedpositions

# assumption: When the stars form a message, they will be at their
# most compact arrangement.
# let's find the time where the delta between the max y and min y is smallest
def minmax(seconds):
    # at a given number of seconds, 
    #   report the minimum and the maximum values
    #   of the x and y values of the stars    
    updatedstars = positions(stars, velocities, seconds)
    min_x = min([s[0] for s in updatedstars])
    max_x = max([s[0] for s in updatedstars])
    min_y = min([s[1] for s in updatedstars])
    max_y = max([s[1] for s in updatedstars])
    return min_x, min_y, max_x, max_y

def display_stars_at(seconds):
    displaystars = positions(stars, velocities, seconds)
    x_offset = min([s[0] for s in displaystars])
    y_offset = min([s[1] for s in displaystars])
    # shift all stars near the origin
    # (and a set gives us faster lookup later)
    displaystars = set([(s[0]-x_offset, s[1]-y_offset) for s in displaystars])
    col_limit = max([s[0] for s in displaystars])
    row_limit = max([s[1] for s in displaystars])
    # build the output
    for i in range(0, row_limit+1):
        outputline = []
        for j in range(0, col_limit+1):
            if (j, i) in displaystars:
                outputline.append('#')
            else:
                outputline.append('.')
        print(''.join(outputline))

lastdelta = float('inf')
i = 0
while True:
    locations = minmax(i)
    nextdelta = abs(locations[3] - locations[1])
    if nextdelta > lastdelta:
        break
    lastdelta = nextdelta
    i += 1

message_time = i-1
print(f'Minimum y delta at {message_time} seconds')
print(minmax(message_time))

display_stars_at(message_time)
print(f'Message appeared at {message_time} seconds')







