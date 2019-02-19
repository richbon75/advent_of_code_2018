class Room(object):
    '''This is the basic room.'''

    # if you enter a room by going N,
    # that means it has a door in the S
    reflect = {
        'N':'S',
        'E':'W',
        'W':'E',
        'S':'N'
    }

    offset = {
        'N': (-1, 0),
        'E': ( 0, 1),
        'W': ( 0,-1),
        'S': ( 1, 0)
    }

    rooms = dict()
 
    limits = {
        'N':0,
        'E':0,
        'W':0,
        'S':0
    }

    def __init__(self, coord=(0,0)):
        self.coord = coord
        self.exits = set()
        self.rooms[coord] = self
        self.update_limits()
        self.doors_from_origin = None
    
    def update_limits(self):
        # Make sure our known limits include this room
        self.limits['N'] = min(self.limits['N'], self.coord[0])
        self.limits['S'] = max(self.limits['S'], self.coord[0])
        self.limits['W'] = min(self.limits['W'], self.coord[1])
        self.limits['E'] = max(self.limits['E'], self.coord[1])
    
    @classmethod
    def enter(cls, coord, entered_as=''):
        if coord in cls.rooms:
            room = cls.rooms[coord]
        else:
            room = Room(coord)
        if entered_as:
            room.exits.add(cls.reflect[entered_as])
        return room

    def mapout(self, direction):
        # if we can leave the room this way,
        # there must be a door
        self.exits.add(direction)
        newcoords = tuple(c+d for c, d in zip(self.coord, self.offset[direction]))
        nextroom = self.enter(coord = newcoords, entered_as = direction)
        return nextroom
    
    def go(self, direction):
        direction = direction.upper()
        if direction in self.exits:
            newcoords = tuple(c+d for c, d in zip(self.coord, self.offset[direction]))
            nextroom = self.enter(coord = newcoords, entered_as = direction)
            return nextroom
        else:
            raise RuntimeError(f'No exit going {direction}')
    
    def __str__(self):
        return f'Room: {self.coord}  Exits: {self.exits}'
    
    def __repr__(self):
        return str(self)
    
def visitall():
    door_distance = 0
    rooms1k = 0
    origin = Room.enter((0,0))
    origin.doors_from_origin = door_distance
    just_visited = [Room.enter((0,0)),]
    while len(just_visited) > 0:
        now_visiting = list()
        for room in just_visited:
            door_distance = room.doors_from_origin + 1
            for direction in room.exits:
                visit = room.go(direction)
                if visit.doors_from_origin is None:
                    if door_distance >= 1000:
                        rooms1k += 1
                    visit.doors_from_origin = door_distance
                    now_visiting.append(visit)
        just_visited = now_visiting
    return door_distance-1, rooms1k

# Some of this function is lifted from a solution found here:
# https://www.reddit.com/r/adventofcode/comments/a7uk3f/2018_day_20_solutions/ec5y3lm

def build_map(expression):
    pos = {Room.enter((0,0)),}    # current positions we're building out
    starts = {Room.enter((0,0)),} # where the current positions started
    ends = set()
    stack = list()
    for c in expression:
        if c in 'NEWS':
            pos = {room.mapout(c) for room in pos}
        if c == '|':
            ends.update(pos)
            pos = starts
        if c == '(':
            stack.append((starts, ends))
            starts, ends = pos, set()
        if c == ')':
            pos.update(ends)
            starts, ends = stack.pop()

if __name__ == "__main__":
    origin = Room.enter((0,0))
    with open('a20_input.txt','r') as f:
        for line in f:
            mapregex = line.strip()
    build_map(mapregex)
    doors_to_furthest_room, rooms1k = visitall()
    print(f'Part 1: Doors to furthest room: {doors_to_furthest_room}')
    print(f'Part 2: Rooms at least 1000 doors away: {rooms1k}')
    '''
    # Test code to wander the rooms
    current_room = origin
    direction = 'N'
    while direction.upper() in 'NEWS':
        print(current_room)
        direction = input('Go where? ')
        try:
            current_room = current_room.go(direction.upper())
        except RuntimeError as err:
            print(err)
    '''


    




        


