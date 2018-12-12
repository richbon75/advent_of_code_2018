
class Marble(object):
    # implement a doubly-linked list.
    def __init__(self, value):
        # Init a single marble with circular references to itself
        self.value = value
        self.left = self
        self.right = self
    
    def displayit(self, current=None):
        print(self.value)
        nextnode = self.right
        while nextnode is not self:
            print(nextnode.value)
            nextnode = nextnode.right

    def insert(self, value):
        # Insert a marble at this spot,
        # push the "current" marble to the right
        # return the new marble reference
        marble = Marble(value)
        marble.left = self.left
        marble.right = self
        self.left = marble
        marble.left.right = marble
        return marble
    
    def remove(self):
        # remove marble, return value and marble to the right
        righty = self.right
        righty.left = self.left
        self.left.right = righty
        return self.value, righty
    
    def travel(self, i):
        # travel to an offset of index i
        # positive values go clockwise, negatives counterclockwise
        current_node = self
        delta = -1 if i > 0 else 1
        while i != 0:
            i += delta
            if delta == -1:
                current_node = current_node.right
            else:
                current_node = current_node.left
        return current_node

def playgame(players, maxmarble):
    # play the game, return the high score
    currentmarble = Marble(0)
    scores = [0 for x in range(0,players)]
    player = 0
    for x in range(1, maxmarble+1):
        if x % 23 != 0:
            currentmarble = currentmarble.right.right.insert(x)
        else:
            y, currentmarble = currentmarble.travel(-7).remove()
            scores[player] += x + y
        player = (player + 1) % players
    return max(scores)

assert playgame(9, 25) == 32
assert playgame(10,1618) == 8317
assert playgame(13, 7999) == 146373
assert playgame(17, 1104) == 2764
assert playgame(21, 6111) == 54718
assert playgame(30, 5807) == 37305

# my input: 468 players; last marble is worth 71010 points
import time
start_time = time.time_ns()
print(f'max score is: {playgame(468, 71010)}')
print(f'elapsed time seconds: {(time.time_ns() - start_time) / 1000000000}')

