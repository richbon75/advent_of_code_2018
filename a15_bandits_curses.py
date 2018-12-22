'''My very first use of the curses library, jammed in after the fact. Don't judge me.'''

import time
import curses
from curses import wrapper

echo_on = False
gstdscr = None

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
    if char == 'E':
        colorcode = curses.color_pair(4)
    elif char == 'G':
        colorcode = curses.color_pair(1)
    elif char == '#':
        colorcode = curses.color_pair(3)
    gstdscr.addch(*cursespos, ord(char), colorcode)

def readingkey(pos): 
    '''Use as key function in "reading-order" sorts.'''
    return (pos[1], pos[0])

def echo(value):
    if echo_on:
        print(value)

big_log = []
log_on = True

def log(value):
    '''A handy way to compare differences between versions.'''
    global big_log
    if log_on:
        big_log.append(value + '\n')

def log_move(move_from, move_to):
    if move_from != move_to:
        log(f'moved {(move_from[0], move_from[1])} to {(move_to[0], move_to[1])}')

def log_attack(attacker, attackee, note = ''):
    log(f'{(attacker[0], attacker[1])} attacks {(attackee[0], attackee[1])}{note}')

def write_log(filename):
    if log_on:
        with open(filename, 'w') as f:
            f.writelines(big_log)

class ElfDeathError(Exception):
    pass

class Creature(object):
    def __init__(self, cave, position, marker, hp = 200, attack=3):
        self.position = position
        self.marker = marker
        self.enemy = 'E' if marker == 'G' else 'G'
        self.hp = 200
        self.attack = cave.elfattack if marker == 'E' else attack
        self.cave = cave
    
    def __str__(self):
        return f'[Creature: {self.position} {self.marker} {self.hp}]'
    
    def __repr__(self):
        return str(self)
    
    def move(self, newpos):
        oldpos = self.position
        # update my own position
        self.position = newpos
        log_move(oldpos, newpos)
        # update my position in the Cave.creatures dictionary and map
        self.cave.creatures.pop(oldpos)
        self.cave.creatures[newpos] = self
        self.cave.locations.pop(oldpos)
        self.cave.locations[newpos] = self.marker
        drawchar(oldpos, ' ')
        drawchar(newpos, self.marker)
        
    
    def attacks(self, target):
        '''self attacks a target creature'''
        target.hp -= self.attack
        # Bring out your dead!
        if target.hp <= 0:
            if target.marker == 'E' and self.cave.elfwin:
                raise ElfDeathError
            # remove the dead creature from the Cave.creatures dictionary and map
            self.cave.creatures.pop(target.position)
            self.cave.locations.pop(target.position)
            drawchar(target.position, ' ')
        log_attack(self.position, target.position)
    
class Cave(object):

    # some ANSI color codes to make it look nice
    markerdraw = {
        'E': '\033[36mE\033[0m', 
        'G': '\033[31mG\033[0m',
        '#': '\033[33m#\033[0m',
        '.': '.',
        '!': '\033[32m!\033[0m'
    }

    def __init__(self):
        self.height = 0
        self.width = 0
        self.locations = dict()
        self.creatures = dict()
        self.rounds = 0
        self.war_is_over = False  # if you want it
        self.elfwin = False
        self.elfattack = 3
    
    def adjacent_spots(self, positions, clear_only=True):
        '''Given a list of positions, return a set of valid adjacent positions.'''
        adj_positions = set([(x+dx, y+dy) for x,y in positions for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]])
        if clear_only:
            adj_positions.difference_update(self.locations)
        return adj_positions

    def get_creature_at(self, position):
        answer = list(filter(lambda c: c.position == position, self.creatures))
        if answer:
            return answer[0]
        return None
    
    def add_location(self, point, marker):
        self.width = max(self.width, point[0]+1)
        self.height = max(self.height, point[1]+1)
        self.locations[point] = marker
        if marker in ('G', 'E'):
            self.creatures[point] = (Creature(self, point, marker))
        drawchar(point, marker)
    
    def print(self, overlay=dict(), highlight=set()):
        # Print out the cave
        for y in range(0, self.height):
            outline = []
            hp_info = []
            for x in range(0, self.width):
                if (x,y) in highlight:
                    outline.append('\033[43m')
                marker = overlay.get((x,y), self.locations.get((x,y), '.'))
                outline.append(self.markerdraw.get(marker, marker))
                if marker in ('G', 'E'):
                    c = self.creatures[(x,y)]
                    hp_info.append(f'{self.markerdraw[c.marker]}({c.hp})')
                if (x,y) in highlight:
                    outline.append('\033[0m')
            print(''.join(outline) + '   ' + ', '.join(hp_info))
    
    def get_shells(self, from_locs, to_locs):
        '''A breadth-first rangefinder. The shells[0] is the set of starting positions,
        shells[1] are the positions that can be reached in one step from shells[0],
        shells[2] are one step from shells[1], etc.'''
        known_locations = set(from_locs)
        shells = [set(known_locations)]
        # shells[-1] is always the last set of positions we added
        while shells[-1] and not shells[-1].intersection(to_locs):
            next_locations = self.adjacent_spots(shells[-1]).difference(known_locations)
            known_locations.update(next_locations)
            shells.append(next_locations)
        if shells[-1]:
            # leave only our matches to the desired destination(s) in the final shell
            shells[-1].intersection_update(to_locs)
            return shells
        return None
    
    def round(self):
        global gstdscr
        '''Fight a round of the war.  Returns False when the war is over, True otherwise.'''
        if self.war_is_over:
            echo('War is over, if you want it.')
            return False
        # each unit alive takes a turn in reading order
        round_info = f'Round {self.rounds+1}'
        log(round_info)
        gstdscr.addstr(0, 0, round_info)
        turns = sorted([c for _, c in self.creatures.items()], key=lambda c: (c.position[1],c.position[0]))
        for creature in turns:
            echo(f'Turn for {creature}')
            # If creature died, no turn.
            if creature.hp <= 0:
                continue
            # Unit identifies all enemy targets
            enemies = list(filter(lambda c: c.marker == creature.enemy and c.hp > 0, self.creatures.values()))
            # if no enemies, combat ends
            if not enemies:
                echo('War is over.')
                self.war_is_over = True
                return False
            # if not in range of enemy, move
            attack_range = self.adjacent_spots([creature.position], clear_only=False)
            if not attack_range.intersection({e.position for e in enemies}):
                possible_moves = self.adjacent_spots([creature.position])
                attackzones = self.adjacent_spots([e.position for e in enemies])
                outbound_shells = self.get_shells(possible_moves, attackzones)
                if not outbound_shells:
                    # not in range, and no path to enemy - no move, no attack
                    continue
                # outbound_shells[-1] has all nearest destinations. Pick the one we want.
                nearest_attackzones = list(outbound_shells[-1])
                nearest_attackzones.sort(key=readingkey)
                chosen_attackzone = nearest_attackzones[0]
                inbound_shells = self.get_shells({chosen_attackzone}, possible_moves)
                possible_moves = list(inbound_shells[-1])
                possible_moves.sort(key=readingkey)
                creature.move(possible_moves[0])
            # if in range of enemy, attack
            attack_range = self.adjacent_spots([creature.position], clear_only=False)
            attack_targets = attack_range.intersection({e.position for e in enemies})
            attack_targets = list(filter(lambda c: c.position in attack_targets, self.creatures.values()))
            if attack_targets:
                attack_targets.sort(key=lambda c: (c.position[1], c.position[0]))
                attack_targets.sort(key=lambda c: c.hp)
                creature.attacks(attack_targets[0])
        self.rounds += 1
        return True

    def score(self):
        hp_left = sum([c.hp for c in self.creatures.values() if c.hp > 0])
        return self.rounds, hp_left

    @classmethod
    def load_cave_from_file(cls, filename, elfattack = None):
        c = Cave()
        if elfattack:
            c.elfwin = True
            c.elfattack = elfattack
        with open(filename, 'r') as f:
            y = 0
            for line in f:
                for x, marker in enumerate(line.strip()):
                    if marker != '.':
                        c.add_location((x,y), marker)
                y += 1
        return c

def elfsurvive(elfattack):
    c = Cave.load_cave_from_file('a15_input.txt', elfattack)
    # print(f'Elfattack = {elfattack}')
    try:
        while c.round():
            pass
    except ElfDeathError:
        # print(f'First Elf died during round {c.rounds+1}')
        return False
    else:
        # print(f'No Elves died!')
        rounds, hp_left = c.score()
        result = f'Rounds: {rounds}  HP: {hp_left}  Outcome: {rounds * hp_left}'
        # print(result)
        return result


log_on = False  # I have a logger I was using to squash bugs, this turns it off.

def main(stdscr):
    global gstdscr
    gstdscr = stdscr       # so I can reach it in other places in the code without passing it around
    curses.curs_set(0)     # hide the cursor
    # stdscr.nodelay(True)   # make stdsrc.getch() non-blocking
    stdscr.clear()
    setcolors()
    # setcolors()
    c = Cave.load_cave_from_file('a15_input.txt')
    while c.round():
        stdscr.refresh()
        time.sleep(0.1)
    rounds, hp_left = c.score()
    results = f'Rounds: {rounds}  HP: {hp_left}  Outcome: {rounds * hp_left}'
    stdscr.addstr(c.height+1, 0, results)
    _ = stdscr.getch()

wrapper(main)
