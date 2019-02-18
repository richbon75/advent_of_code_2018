'''
Let's make a fun animated curses version again.

  . open ground
  | trees
  # lumberyard

'''

import time
from collections import Counter
import curses
from curses import wrapper

gstdscr = None
ground = dict()
maxy = -float('inf')
maxx = -float('inf')

def import_ground(filename):
    global maxx, maxy
    ground = dict()
    with open(filename, 'r') as f:
        y = -1
        for line in f:
            y+=1
            x=0
            line = line.strip()
            for x, char in enumerate(line):
                ground[(x,y)] = char
                maxy = max(maxy,y)
                maxx = max(maxx,x)
                drawchar((x,y), char)
    return ground

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
        c = newthing(ground, pos)
        nextground[pos] = c
        drawchar(pos, c)
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

# gprint(ground)
last_resource = 0
for m in range(1,11):
    # print(f'\n\nMinute: {m}')
    ground = minute(ground)
    # gprint(ground)
    this_resource = resource(ground)
    print(f'Minute: {m}  Resource: {this_resource}\n')
    last_resource = this_resource
print('all done')

def setcolors():
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_CYAN, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)

def drawchar(pos, char, color=None):
    global gstdscr
    cursespos = (pos[1]+1, pos[0])   # Curses positions are (y,x)
    colorcode = curses.color_pair(0)
    if char == '.':
        colorcode = curses.color_pair(0)
    elif char == '#':
        colorcode = curses.color_pair(4)
    elif char == '|':
        colorcode = curses.color_pair(3)
    # If you're getting an exception here, your output screen is
    # probably too small for the output to redner - try making
    # the terminal window bigger or the font smaller.
    gstdscr.addch(*cursespos, ord(char), colorcode)

def main(stdscr):
    global gstdscr, ground
    gstdscr = stdscr       # so I can reach it in other places in the code without passing it around
    curses.curs_set(0)     # hide the cursor
    stdscr.clear()
    setcolors()
    stdscr.addstr(0, 0, 'Minute: 0')
    ground = import_ground('a18_input.txt')
    for m in range(0,1000):
        ground = minute(ground)
        stdscr.addstr(0, 0, f'Minute: {m}')
        stdscr.refresh()
        # time.sleep(0.1)
    _ = stdscr.getch()  # press any key to continue

wrapper(main)
