'''Improved version:
Rather than implement my own doubly-linked list,
use a containers.deque to store the game data.
The "curent node" is simply the end of the list, and
traversing the circular list is just moving items from
the end to the beginning of the deque (or vice-versa)'''

from collections import deque

def playgame(players, maxmarble):
    # play the game, return the high score
    game = deque([0])
    scores = [0 for x in range(0,players)]
    player = 0
    for x in range(1, maxmarble+1):
        if x % 23 != 0:
            game.rotate(-2)
            game.appendleft(x)
        else:
            game.rotate(7)
            y = game.popleft()
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
# day two: last marble is worth 7101000

import time
start_time = time.time_ns()
print(f'max score is: {playgame(468, 7101000)}')
print(f'elapsed time seconds: {(time.time_ns() - start_time) / 1000000000}')


