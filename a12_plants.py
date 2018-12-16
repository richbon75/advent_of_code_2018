from collections import deque

rules = dict()

with open('a12_input.txt') as f:
    init_state = f.readline()
    init_state = init_state.strip().split()[2]
    f.readline()
    for line in f:
        parts = line.strip().split()
        rules[parts[0]] = parts[2]

current_state = list(init_state)

def nextgen(current_state, potzero_offset = None):
    '''Apply the rules to generate the next state, given the current state'''
    if potzero_offset is None:
        potzero_offset = 0
    potzero_offset -= 2
    next_state = deque()
    test_frame = deque('.....')
    for pot in current_state:
        test_frame.append(pot)
        test_frame.popleft()
        next_state.append(rules.get(''.join(test_frame),'.'))
    for pot in '.....':
        test_frame.append(pot)
        test_frame.popleft()
        next_state.append(rules.get(''.join(test_frame),'.'))
    # Trim empty pots from the ends of the next state
    while next_state[0] == '.':
        next_state.popleft()
        potzero_offset += 1
    while next_state[-1] == '.':
        next_state.pop()
    return next_state, potzero_offset

def potsum(current_state, potzero_offset):
    psum = 0
    for pnum in range(potzero_offset, len(current_state)+potzero_offset):
        if current_state[0] == '#':
            psum += pnum
        current_state.rotate(-1)
    return psum

print(''.join(current_state))
potzero_offset = None
for gen in range(0,20):
   current_state, potzero_offset = nextgen(current_state, potzero_offset)
   print(gen+1, potzero_offset, potsum(current_state, potzero_offset), ''.join(current_state))

print(f'After 20 generations, the sum of the numbers of all pots which contain a plant:')
print(potsum(current_state, potzero_offset))





