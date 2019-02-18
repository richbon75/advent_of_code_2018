import time
from collections import Counter
import curses
from curses import wrapper

gstdscr = None

class Ground(object):
    
    def __init__(self, maxx = -float('inf'), maxy = -float('inf')):
        self.g = dict()
        self.maxx = maxx
        self.maxy = maxy

    @classmethod
    def loadfromfile(cls, filename):
        ground = Ground()
        with open(filename, 'r') as f:
            y = -1
            for line in f:
                y+=1
                x=0
                line = line.strip()
                for x, char in enumerate(line):
                    ground.maxy = max(ground.maxy,y)
                    ground.maxx = max(ground.maxx,x)
                    ground.setGround((x,y), char)
        return ground
    
    def setGround(self, pos, marker):
        self.g[pos] = marker
        drawchar(pos, marker)
    
    def survey(self):
        return Counter([m for m in self.g.values()])
    
    def minute(self):
        '''Iterate one minute'''
        nextGround = dict()
        for y in range(0, self.maxy+1):
            around = Counter()
            for x in range(-1, self.maxx+1):
                marker = self.g.get((x,y), None)
                n = x+1
                # add the 3 ahead and one behind me
                around.update((self.g.get((n,y-1),None), self.g.get((n,y), None), self.g.get((n,y+1),None), self.g.get((x-1, y), None)))
                n = x-2
                # remove the 3 two behind and remove myself
                around.subtract((self.g.get((n,y-1),None), self.g.get((n,y), None), self.g.get((n,y+1),None), marker))
                if x < 0:
                    continue
                marker = self.g[(x,y)]
                if marker == '.' and around['|'] >= 3:
                    marker = '|'
                elif marker == '|' and around['#'] >= 3:
                    marker = '#'
                elif marker == '#' and (around['#'] == 0 or around['|'] == 0):
                    marker = '.'
                nextGround[(x,y)] = marker
                drawchar((x,y), marker)
        self.g = nextGround
    
    def print(self):
        print('\n\n\n')
        for y in range(0, self.maxy+1):
            outline = []
            for x in range(0, self.maxx+1):
                outline.append(self.g.get((x,y), 'x'))
            print(''.join(outline))

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
    ground = Ground.loadfromfile('a18_input.txt')
    stdscr.refresh()
    for m in range(0,1000):
        ground.minute()
        stdscr.addstr(0, 0, f'Minute: {m}')
        # time.sleep(0.1)
        stdscr.refresh()
    _ = stdscr.getch()  # press any key to continue
    # c = ground.survey()
    # print(c['|'] * c['#'])

wrapper(main)

                



