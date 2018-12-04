import re

regex = r"^#(?P<code>\d+) @ (?P<col>\d+),(?P<row>\d+): (?P<width>\d+)x(?P<height>\d+)"

class Fabric:

    def __init__(self):
        self.fabric = [ [ 0 for i in range(1000) ] for j in range(1000) ]
        self.overlaps = 0

    def update(self, row, col, width, height):
        for i in range(row, row + height):
            for j in range(col, col + width):
                self.fabric[i][j] += 1
                if self.fabric[i][j] == 2:
                    self.overlaps += 1
    
    def was_overlapped(self, row, col, width, height):
        overlapped = False
        for i in range(row, row + height):
            for j in range(col, col + width):
                overlapped = overlapped or bool(self.fabric[i][j] - 1)
        return overlapped

fabric = Fabric()
f = open('a03_input.txt', 'r')
for line in f:
    m = re.match(regex, line.strip()).groupdict()
    fabric.update(int(m['row']), int(m['col']), int(m['width']), int(m['height']))
f.close()

f = open('a03_input.txt', 'r')
for line in f:
    m = re.match(regex, line.strip()).groupdict()
    if not fabric.was_overlapped(int(m['row']), int(m['col']), int(m['width']), int(m['height'])):
        print(f"Overlap free: {m['code']}")
f.close()

print(f'Answer: {fabric.overlaps}')

