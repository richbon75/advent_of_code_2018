# My Input ########
my_depth = 3879
my_target = (8, 713)

# Note: My answer for day 2 comes out as the correct answer - 1.
# Not sure why.  Don't feel like digging through it right now.
# Also, runs much faster with pypy

###################

class Cave(object):

    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        self.geologic_index = {
            (0,0):0,
            target: 0}
        self.erosion_levels = {}
        self.types = {}
        self.type_names = ['rocky', 'wet', 'narrow']
        self.type_symbol = ['.', '=', '|']
        self.time_to = {(0,0):0}

    def get_geologic(self, loc):
        if loc not in self.geologic_index:
            if loc[1] == 0:
                self.geologic_index[loc] = loc[0] * 16807
            elif loc[0] == 0:
                self.geologic_index[loc] = loc[1] * 48271
            else:
                self.geologic_index[loc] = (self.get_erosion((loc[0]-1, loc[1])) *
                                    self.get_erosion((loc[0], loc[1]-1)))
        return self.geologic_index[loc]

    def get_erosion(self, loc):
        if loc not in self.erosion_levels:
            self.erosion_levels[loc] = (self.get_geologic(loc) + self.depth) % 20183        
        return self.erosion_levels[loc]

    def get_type(self, loc):
        if loc not in self.types:
            self.types[loc] = self.get_erosion(loc) % 3
        return self.types[loc]
    
    def get_type_name(self, loc):
        return self.type_names[self.get_type(loc)]
    
    def get_type_symbol(self, loc):
        return self.type_symbol[self.get_type(loc)]

    def risk_level(self, from_loc=(0,0), to_loc=None):
        if to_loc is None:
            to_loc = self.target
        risk = 0
        for x in range(from_loc[0], to_loc[0]+1):
            for y in range(from_loc[1], to_loc[1]+1):
                risk += self.get_type((x,y))
        return risk
    
    def print(self, from_loc=(0,0), to_loc=None):
        if to_loc is None:
            to_loc = self.target
        caverows = list()
        for y in range(from_loc[1], to_loc[1]+1):
            rowout = list()
            for x in range(from_loc[0], to_loc[0]+1):
                rowout.append(self.get_type_symbol((x,y)))
            caverows.append(''.join(rowout))
        print('\n'.join(caverows))
            

class Explorer(object):

    tools = { #cave.type_names = ['rocky', 'wet', 'narrow']
        'torch':{0, 2},          # rocky, narrow
        'climbing_gear':{0, 1},  # rocky, wet
        'neither':{1, 2}         # wet, narrow
    }

    allowed_tools = {
        0 : {'torch', 'climbing_gear'},
        1 : {'climbing_gear', 'neither'},
        2 : {'torch', 'neither'}
    }

    def __init__(self, cave):
        self.current_tool = 'torch'
        self.cave = cave
        self.loc = (0,0)
        self.best_times = {
            ((0,0),'torch'): 0
        }
        self.edges = [((0,0),'torch')]
        self.next_edges = set()
    
    def visit_edge(self):
        current_loc, current_tool = self.edges.pop()
        current_time = self.best_times[(current_loc, current_tool)]
        cheap_moves, swap_moves = self.moves(current_loc, current_tool)
        cheap_cases = [(m, current_tool) for m in cheap_moves]
        swap_cases = list()
        for m in swap_moves:
            for n in self.get_allowed_tools(m):
                swap_cases.append((m, n))
        for c in cheap_cases:
            if c not in self.best_times or self.best_times[c] > current_time+1:
                self.best_times[c] = current_time + 1
                self.next_edges.add(c)
        for c in swap_cases:
            if c not in self.best_times or self.best_times[c] > current_time+8:
                self.best_times[c] = current_time + 8
                self.next_edges.add(c)
    
    def visit_all_edges(self):
        while self.edges:
            self.visit_edge()
        self.edges = list(self.next_edges)
        self.next_edges = set()
    
    def explore(self):
        round = 0
        while self.edges:
            print(f'{round}  Edges to visit: {len(self.edges)}')
            self.visit_all_edges()
            round += 1
    
    def neighbors(self, loc=None):
        # What are valid neighbors of this cell?
        # let's also add some bounding around the cave, so
        # we can't go off into infinity
        if loc is None:
            loc = self.loc
        neighbors = {
            (loc[0]+off[0], loc[1]+off[1]) \
                for off in ((-1,0),(1,0),(0,-1),(0,1)) \
                if loc[0]+off[0] >= 0 and loc[1]+off[1] >= 0
                   and loc[0]+off[0] < self.cave.target[0] + 200
                   and loc[1]+off[1] < self.cave.target[1] + 200
        }
        return neighbors
    
    def get_allowed_tools(self, loc):
        # for a given loc, what tools are allowed?
        if loc in {(0,0), self.cave.target}:
            return {'torch'}
        return self.allowed_tools[self.cave.get_type(loc)]
    
    def moves(self, loc=None, tool=None):
        if loc is None:
            loc = self.loc
        if tool is None:
            tool = self.current_tool
        all_moves = self.neighbors(loc)
        # Split into sets of moves I can make without
        # swapping tools, and moves that require changing
        cheap_moves = {m for m in all_moves \
            if tool in self.get_allowed_tools(m)}
        swap_moves = all_moves.difference(cheap_moves)
        return (cheap_moves, swap_moves)
    


if __name__ == "__main__":
    '''
    # Tests from problem description
    cave = Cave(510, (10,10))
    assert cave.get_geologic((0,0)) == 0
    assert cave.get_erosion((0,0)) == 510
    assert cave.get_type((0,0)) == 0
    assert cave.get_geologic((1,1)) == 145722555
    assert cave.get_erosion((1,1)) == 1805
    assert cave.get_type((1,1)) == 2
    assert cave.risk_level() == 114
    # cave.print((0,0),(15,15))
    '''

    # My cave
    mycave = Cave(my_depth, my_target)
    print(f'Day One answer: {mycave.risk_level()}')
    mycave.print()
    me = Explorer(mycave)
    me.explore()
    print(f'Day Two answer: {me.best_times[(mycave.target, "torch")]}')
    print("Note: In my run, this answer is -1 below the correct answer.")
    print("Not sure why. Don't have time to fix it now.")
    




