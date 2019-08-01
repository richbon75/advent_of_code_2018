import re

class Nanobot(object):
    def __init__(self, x, y, z, r):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.r = int(r)
    
    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def in_range(self, other):
        return (self.manhattan_distance(other) <= self.r)

    def __str__(self):
        return f'pos=<{self.x},{self.y},{self.z}>, r={self.r}'

    def __repr__(self):
        return f'Nanobot("{str(self)}")'

if __name__ == "__main__":

    swarm = []

    with open('a23_input.txt', 'r') as f:
        nanore = re.compile(r'pos=<(-*\d+),(-*\d+),(-*\d+)>, r=(-*\d+)')
        for line in f:
            match = re.match(nanore, line)
            if match:
                swarm.append(Nanobot(match.group(1),match.group(2),match.group(3),match.group(4)))
    
    print('Part 1')
    max_r = max([n.r for n in swarm])
    strongest = [n for n in swarm if n.r == max_r][0]
    print(f'Strongest nanobot: {strongest}')
    in_range = [n for n in swarm if strongest.in_range(n)]
    print(f'Nanobots in range: {len(in_range)}')
    



