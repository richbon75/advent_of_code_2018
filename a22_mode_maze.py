# My Input ########
my_depth = 3879
my_target = (8, 713)
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

    def risk_level(self, from_loc=(0,0), to_loc=None):
        if to_loc is None:
            to_loc = self.target
        risk = 0
        for x in range(from_loc[0], to_loc[0]+1):
            for y in range(from_loc[1], to_loc[1]+1):
                risk += self.get_type((x,y))
        return risk

if __name__ == "__main__":
    # Tests from problem description
    cave = Cave(510, (10,10))
    assert cave.get_geologic((0,0)) == 0
    assert cave.get_erosion((0,0)) == 510
    assert cave.get_type((0,0)) == 0
    assert cave.get_geologic((1,1)) == 145722555
    assert cave.get_erosion((1,1)) == 1805
    assert cave.get_type((1,1)) == 2
    assert cave.risk_level() == 114

    # My cave
    mycave = Cave(my_depth, my_target)
    print(f'Day One answer: {mycave.risk_level()}')
    




