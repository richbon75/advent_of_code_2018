echo_on = False

def readingkey(pos):
    '''Use as key function in "reading-order" sorts.'''
    return (pos[1], pos[0])

def echo(value):
    if echo_on:
        print(value)

big_log = []

def log(value):
    '''A handy way to compare differences between versions.'''
    global big_log
    big_log.append(value + '\n')

def log_move(move_from, move_to):
    if move_from != move_to:
        log(f'moved {(move_from[0], move_from[1])} to {(move_to[0], move_to[1])}')

def log_attack(attacker, attackee, note = ''):
    log(f'{(attacker[0], attacker[1])} attacks {(attackee[0], attackee[1])}{note}')

def write_log(filename):
    with open(filename, 'w') as f:
        f.writelines(big_log)

class Creature(object):
    def __init__(self, cave, position, marker, hp = 200, attack=3):
        self.position = position
        self.marker = marker
        self.enemy = 'E' if marker == 'G' else 'G'
        self.hp = hp
        self.attack = attack
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
        
    
    def attacks(self, target):
        '''self attacks a target creature'''
        target.hp -= self.attack
        # Bring out your dead!
        if target.hp <= 0:
            # remove the dead creature from the Cave.creatures dictionary and map
            self.cave.creatures.pop(target.position)
            self.cave.locations.pop(target.position)
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
    
    def print(self, overlay=dict()):
        # Print out the cave
        for y in range(0, self.height):
            outline = []
            hp_info = []
            for x in range(0, self.width):
                marker = overlay.get((x,y), self.locations.get((x,y), '.'))
                outline.append(self.markerdraw.get(marker, marker))
                if marker in ('G', 'E'):
                    c = self.creatures[(x,y)]
                    hp_info.append(f'{self.markerdraw[c.marker]}({c.hp})')
            print(''.join(outline) + '   ' + ', '.join(hp_info))
    
    def get_shells(self, from_locs, to_locs):
        '''A breadth-first rangefinder. The shells[0] is the set of starting positions,
        shells[1] are the positions that can be reached in one step from shells[0],
        shells[2] are one step from shells[1], etc.'''
        known_locations = set(from_locs)
        shells = [known_locations]
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
        '''Fight a round of the war.  Returns False when the war is over, True otherwise.'''
        if self.war_is_over:
            echo('War is over, if you want it.')
            return False
        # each unit alive takes a turn in reading order
        log(f'Round {self.rounds+1}')
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
                inbound_shells = self.get_shells(outbound_shells[-1], possible_moves)
                possible_moves = list(inbound_shells[-1])
                possible_moves.sort(key=readingkey)
                creature.move(possible_moves[0])
            # if in range of enemy, attack
            attack_range = self.adjacent_spots([creature.position], clear_only=False)
            attack_targets = attack_range.intersection({e.position for e in enemies})
            attack_targets = list(filter(lambda c: c.position in attack_targets, self.creatures.values()))
            if attack_targets:
                attack_targets.sort(key=lambda c: c.hp)
                creature.attacks(attack_targets[0])
        self.rounds += 1
        return True

    def score(self):
        hp_left = sum([c.hp for c in self.creatures.values() if c.hp > 0])
        return self.rounds, hp_left

    @classmethod
    def load_cave_from_file(cls, filename):
        c = Cave()
        with open(filename, 'r') as f:
            y = 0
            for line in f:
                for x, marker in enumerate(line.strip()):
                    if marker != '.':
                        c.add_location((x,y), marker)
                y += 1
        return c

c = Cave.load_cave_from_file('a15_input.txt')
while c.round():
    pass
# write_log('a15_mylog2.txt')
rounds, hp_left = c.score()
print(rounds, hp_left, rounds * hp_left)




