
def leftof(pos):
    return (pos[0]-1, pos[1])

def rightof(pos):
    return (pos[0]+1, pos[1])

def below(pos):
    return (pos[0], pos[1]+1)

def extract_range(value):
    '''input a string like '25' or '25..29'
    and an appropriate range() will be generated'''
    vals = value.split('..')
    if len(vals) == 1:
        return range(int(vals[0]), int(vals[0])+1)
    return range(int(vals[0]), int(vals[1])+1)

class Ground(object):
    def __init__(self):
        self.ground = dict()
        self.miny = float('inf')
        self.maxy = -float('inf')
        self.minx = float('inf')
        self.maxx = -float('inf')
        self.spring_pos = None
        self.dripzone = [] # places water is falling from that we haven't evaluated yet
    
    def add_spring(self, x=500):
        '''Add the water source. Don't modify miny.'''
        self.spring_pos = (x, self.miny-1)
        self.ground[self.spring_pos] = '+'
        self.dripzone.append(self.spring_pos)
    
    def get(self, pos):
        return self.ground.get(pos, '.')
    
    def setground(self, pos, marker):
        '''update a map position'''
        self.ground[pos] = marker
        self.minx = min(self.minx, pos[0])
        self.maxx = max(self.maxx, pos[0])
        self.miny = min(self.miny, pos[1])
        self.maxy = max(self.maxy, pos[1])
    
    def clayline(self, line):
        '''read in a line of clay'''
        line = line.strip()
        line = line.split(', ')
        line.sort(key = lambda m: m[0]) # puts x term first.
        xs = extract_range(line[0].split('=')[1])
        ys = extract_range(line[1].split('=')[1])
        for x in xs:
            for y in ys:
                self.setground((x,y), '#')
    
    def print(self):
        '''print out the ground'''
        rows = 0
        for y in range(self.miny-1, self.maxy+1):
            outrow = []
            for x in range(self.minx, self.maxx+1):
                outrow.append(self.ground.get((x,y), '.'))
            rows += 1
            print(''.join(outrow) + str(y))
            if rows % 500 == 0:
                _ = input('Press enter to continue.')
    
    def drip(self):
        '''Flow the water from a dripzone. Returns number of created dripzones.'''
        newdrips = 0
        # Get the next drip
        if not self.dripzone:
            print('No more dripzones! All done.')
            return -1
        dripfrom = self.dripzone.pop()
        x, y = dripfrom        
        # Fall until we hit a surface (or water we've already drawn)
        while y+1 <= self.maxy and self.get(below((x,y))) == '.':
            y += 1
            self.setground((x,y), '|')
        if y == self.maxy or self.get(below((x,y))) in ('|'):
            # dripped beyond maxy or into existing flowing water, no more drips from here
            return newdrips
        # Fill up the container we've fallen into
        top_found = False
        while not top_found:
            left_side_solid = False
            left_x = None
            right_side_solid = False
            right_x = None
            # find the left side - keep going left as long as the
            # left side is clear and there is clay or standing water beneath
            while self.get(leftof((x,y))) in ('.', '|') and self.get(below(leftof((x,y)))) in ('#','~'):
                x -= 1
            if self.get(leftof((x,y))) == '.' and self.get(below(leftof((x,y)))) == '.':
                # the next location the the left is a drop
                x -= 1
                left_side_solid = False
                left_x = x
                self.dripzone.append((x,y))
                newdrips += 1
            elif self.get(leftof((x,y))) == '|':
                # left side is an existing drop, which has already been calculated, so no new drop.
                left_side_solid = False
                left_x = x
            elif self.get(leftof((x,y))) == '#':
                # we've found the closed left side of the container
                left_side_solid = True
                left_x = x
            else:
                raise RuntimeError(f"LEFT: This was unexpected. {(x, y)}")
            # figure out what's on the right side
            x = dripfrom[0] # back to where we dripped from
            while self.get(rightof((x,y))) in ('.', '|') and self.get(below(rightof((x,y)))) in ('#','~'):
                x += 1
            if self.get(rightof((x,y))) == '.' and self.get(below(rightof((x,y)))) == '.':
                # the next location the the right is a drop
                x += 1
                right_side_solid = False
                right_x = x
                self.dripzone.append((x,y))
                newdrips += 1
            elif self.get(rightof((x,y))) == '|':
                # right side is an existing drop, which has already been calculated, so no new drop.
                right_side_solid = False
                right_x = x
            elif self.get(rightof((x,y))) == '#':
                # we've found the closed right side of the container
                right_side_solid = True
                right_x = x
            else:
                raise RuntimeError(f"RIGHT: This was unexpected. {(x, y)}")
            # fill in the level we're at
            if left_side_solid and right_side_solid:
                marker = '~'
            else:
                marker = '|'
            for x in range(left_x, right_x+1):
                self.setground((x,y), marker)
            # if we filled this up, let's try and fill the next level up, too.
            top_found = not(left_side_solid and right_side_solid)
            x = dripfrom[0]
            y -= 1
            if y < self.miny:
                top_found = True
        # Done processing this drip
        assert newdrips <= 2
        return newdrips
    
    def process_all_drips(self):
        '''Keep processing drips untill there are no more.'''
        total_drips_processed = 0
        while self.dripzone:
            # print(f'Drip #{total_drips_processed}   Drips remaining: {len(self.dripzone)}')
            self.drip()
            total_drips_processed += 1
        # print(f'Total drips processed = {total_drips_processed}')
    
    def element_count(self, elements):
        '''Count all the elements of the given types'''
        e_count = 0
        for x in self.ground.values():
            if x in elements:
                e_count += 1
        return e_count

def read_clay(filename):
    ground = Ground()
    with open(filename, 'r') as f:
        for line in f:
            ground.clayline(line)
    return ground


g = read_clay('a17_input.txt')
g.add_spring()
g.process_all_drips()

print(f"PART I: Number of water elements: {g.element_count(('~','|'))}")
print(f"PART II: Retained water: {g.element_count(('~'))}")


        


            
            

            


