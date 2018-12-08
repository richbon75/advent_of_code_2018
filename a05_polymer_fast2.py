# This is a much faster version.
# Pop and append are O(1) time, and should only make one pass through the list
# for a new performance in O(N) time.
# Slow version used lots of slices which are each O(N) time,
# and lots of passes through the list for at least O(N^2) time.

import time, string
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
    reacted = []
    for i in range(0, len(polymer)):
        if reacted and areReactable(reacted[-1], polymer[i]):
            reacted.pop()
            continue
        reacted.append(polymer[i])
    return reacted

def removeUnit(polymer, unit):
    # Given a polymer and the unit letter, remove all instances of that letter.
    # return as a new list
    scrubbed = []
    unit = unit.upper()
    for x in polymer:
        if x.upper() != unit:
            scrubbed.append(x)
    return scrubbed

shortest_length = len(polymer)
for ch in string.ascii_uppercase:
    shortest_length = min(shortest_length, len(react(removeUnit(polymer, ch))))

print(f'elapsed time seconds: {(time.time_ns() - start_time) / 1000000000}')
print(f'Shortest possible length: {shortest_length}')

