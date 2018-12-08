# This is my first version of the solution.
# It is dirt slow because of all the full passes through the polymer


import time
start_time = time.time_ns()

f = open('a05_input.txt', 'r')
for line in f:
    polymer = line.strip()
f.close()

polymer = list(polymer)
# polymer = list('dabAcCaCBAcCcaDA')

def areReactable(a,b):
    # given two units, determine if they are reactable or not
    return (a.upper() == b.upper() and a != b)

def findReactable(polymer):
    # scan the polymer and return the index of the second reactable
    # position or None if no reaction is possible
    for i in range(1,len(polymer)):
        if areReactable(polymer[i-1], polymer[i]):
            return i
    return None

def chainreact(polymer):
    # Find the first reactable index, then reduce the
    # polymer by as much as it can by chain reacting
    units_removed = 0
    toindex = findReactable(polymer)
    if not toindex:
        return units_removed
    fromindex = toindex - 1
    units_removed += 2
    while (fromindex-1 >= 0 and toindex+1 < len(polymer)
           and areReactable(polymer[fromindex-1], polymer[toindex+1])):
           fromindex -= 1
           toindex += 1
           units_removed += 2
    del polymer[fromindex:toindex+1]
    return units_removed

print(len(polymer))
print(findReactable(polymer))

chain_rounds = 0
reactions_remaining = True
while (reactions_remaining):
    chain_rounds += 1
    # print(f'Round: {chain_rounds}')
    # print(f'Polymer starting length: {len(polymer)}')
    removed = chainreact(polymer)
    # print(f'Units removed: {removed}')
    # print(f'Polymer ending length: {len(polymer)}')
    if removed == 0:
        reactions_remaining = False

print(f'elapsed time seconds: {(time.time_ns() - start_time) / 1000000000}')
print(f'Finaly length: {len(polymer)}')

# Pass through polymer ONCE, removing letters as I go,
#  New polymer    <-  investigate letter   <-  old polymer

# test time:  215.578251

