'''
  . open ground
  | trees
  # lumberyard

'''
from collections import Counter

ground = dict()
maxy = -float('inf')
maxx = -float('inf')

def surrounding_pos(ground, pos):
    'Given a position, return the surrounding positions'
    return  [(dx + pos[0], dy + pos[1]) for 
                dx, dy in ((-1,-1,),(0,-1),(1,-1),
                            (-1, 0),        (1, 0),
                            (-1, 1), (0, 1),(1, 1))
                if ((dx + pos[0]) >= 0 and (dx + pos[0]) <= maxx and
                    (dy + pos[1]) >= 0 and (dy + pos[1]) <= maxy)]

def whatsaround(ground, pos):
    w = Counter((ground[xy] for xy in surrounding_pos(ground, pos)))
    return w

def newthing(ground, pos):
    w = whatsaround(ground, pos)
    if ground[pos] == '.' and w['|'] >= 3:
        return '|'
    if ground[pos] == '|' and w['#'] >= 3:
        return '#'
    if ground[pos] == '#' and (w['#'] == 0 or w['|'] == 0):
        return '.'
    return ground[pos]

def minute(ground):
    nextground = dict()
    for pos in ground:
        nextground[pos] = newthing(ground, pos)
    return nextground

def resource(ground):
    c = Counter([g for g in ground.values()])
    # print(c, f"Resource value: {c['|'] * c['#']}")
    return c['|'] * c['#']

def gprint(ground):
    for y in range(0, maxy+1):
        outline = []
        for x in range(0, maxx+1):
            outline.append(ground.get((x,y), 'x'))
        print(''.join(outline))

def main():
    global ground, maxx, maxy
    with open('a18_input.txt', 'r') as f:
        y = -1
        for line in f:
            y+=1
            x=0
            line = line.strip()
            for x, char in enumerate(line):
                ground[(x,y)] = char
                maxy = max(maxy,y)
                maxx = max(maxx,x)
    # gprint(ground)
    # last_resource = 0
    for m in range(0,10):
        # print(f'\n\nMinute: {m}')
        ground = minute(ground)
        # gprint(ground)
        # this_resource = resource(ground)
        print(f'Minute: {m+1}  Resource: {resource(ground)}\n')
        # last_resource = this_resource
    print(resource(ground))

main()

