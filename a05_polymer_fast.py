# This is a much faster version.
# Pop and append are O(1) time, and should only make one pass
# through the list for a new performance in O(N) time.
# Slow version used lots of slices which are each O(N) time,
# and lots of passes through the list for at least O(N^2) time.

import time
start_time = time.time_ns()

f = open('a05_input.txt', 'r')
for line in f:
    polymer = line.strip()
f.close()

polymer = list(polymer)

def areReactable(a,b):
    # given two units, determine if they are reactable or not
    return (a.upper() == b.upper() and a != b)

def react(polymer):
    # Given the original polymer, return a new, fully reacted polymer.
    i = 0
    reacted = []
    for i in range(0, len(polymer)):
        if reacted and areReactable(reacted[-1], polymer[i]):
            reacted.pop()
            continue
        reacted.append(polymer[i])
    return reacted

polymer = react(polymer)

print(f'elapsed time seconds: {(time.time_ns() - start_time) / 1000000000}')
print(f'Final length: {len(polymer)}')

# elapsed time seconds: 0.22385
