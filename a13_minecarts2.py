'''I forgot to save my part 1 and part 2 solutions separately,
so this is the same file for part 1 and part 2'''

class Cart(object):

    all_carts = []

    all_crashes = []

    direction_update = {
        '^': (0, -1),
        'v': (0,  1),
        '<': (-1, 0),
        '>': ( 1, 0)
    }

    intersection_cycle = {
        '<': '|',
        '|': '>',
        '>': '<'
    }

    turn_lookup = {
        # (current direction, next track): next direction
        ('>','-'): '>',
        ('>','/'): '^',
        ('>','\\'): 'v',
        ('<','/'): 'v',
        ('<','\\'): '^',
        ('<','-'): '<',
        ('^','/'): '>',
        ('^','\\'): '<',
        ('^','|'): '^',
        ('v','|'): 'v',
        ('v','\\'): '>',
        ('v','/'): '<'
    }

    directions = ['<','^','>','v']

    dirdelta = {
        '<': -1,
        '|': 0,
        '>': 1
    }

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.next_turn = '<'
        self.all_carts.append(self)
        self.destroyed = False
    
    def __str__(self):
        return f'Cart: {(self.x, self.y)} Direction: {self.direction} Next turn: {self.next_turn}'
    
    def __repr__(self):
        return self.__str__()
   
    def intersect(self):
        '''At an intersection, make the appropriate turn.'''
        i = self.directions.index(self.direction)
        self.direction = self.directions[(self.dirdelta[self.next_turn] + i) % 4]
        self.next_turn = self.intersection_cycle[self.next_turn]
    
    def travel(self, tracks):
        '''Look up the next section of track and travel it.'''
        if self.destroyed:
            return
        dx, dy = self.direction_update[self.direction]
        self.x += dx
        self.y += dy
        if self.collision():
            return
        next_track = tracks[(self.x, self.y)]
        if next_track == '+':
            self.intersect()
        else:
            self.direction = self.turn_lookup[(self.direction, next_track)]
    
    def collision(self):
        '''Check against other carts and see if we've crashed into one.'''
        for cart in self.all_carts:
            if cart is not self and not cart.destroyed:
                if cart.x == self.x and cart.y == self.y:
                    self.all_crashes.append((self.x, self.y))
                    self.destroyed = True
                    cart.destroyed = True
                    print(f'CRASH AT {(self.x, self.y)}!')
                    return True
        return False
    
    @classmethod
    def update_carts(cls, tracks):
        '''FROM PROBLEM STATEMENT (emphasis mine):
        [Carts] take turns moving a single step at a time. They do this
        based on their **current location**: carts on the top row move first
        (acting from left to right), then carts on the second row move
        (again from left to right), then carts on the third row, and so on.

        ***So I need to sort these carts before moving them.'''

        cls.all_carts.sort(key=lambda c: c.x + c.y * width)

        for cart in cls.all_carts:
            cart.travel(tracks)

        # remove destroyed carts
        cls.all_carts = [cart for cart in cls.all_carts if not cart.destroyed]

def print_track(tracks):
    '''This just lets me visualize the current state of the track.
    Not necessary for solving, but nice for debugging.'''
    crash_overlay = dict()
    cart_overlay = dict()
    for crash in Cart.all_crashes:
        crash_overlay[(crash[0], crash[1])] = 'X'
    for cart in Cart.all_carts:
        cart_overlay[(cart.x,cart.y)] = cart.direction
    for y in range(0, height):
        outline = []
        for x in range(0, width):
            outline.append(crash_overlay.get((x,y),cart_overlay.get((x,y),tracks.get((x,y), ' '))))
        print(''.join(outline))

tracks = dict()
width = -float('inf')
height = 0

with open('a13_input.txt', 'r') as f:
    y = -1
    for line in f:
        line = line.rstrip()
        y += 1
        for x, track in enumerate(line):
            if track == ' ':
                continue
            if track in ('<','>'):
                Cart(x, y, track)
                track = '-'
            elif track in ('^', 'v'):
                Cart(x, y, track)
                track = '|'
            tracks[(x,y)] = track
            width = max(width,x)
    height = y + 1
    width = width + 1

print(f'track is: {width}x{height}')
print_track(tracks)

while len(Cart.all_carts) > 1:
    Cart.update_carts(tracks)

print(f'Location of first crash: {Cart.all_crashes[0]}')
print(f'Location of last cart: {(Cart.all_carts[0].x, Cart.all_carts[0].y)}')











