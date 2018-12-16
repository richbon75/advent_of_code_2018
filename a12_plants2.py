from collections import deque

rules = dict()

with open('a12_input.txt') as f:
    init_state = f.readline()
    init_state = init_state.strip().split()[2]
    f.readline()
    for line in f:
        parts = line.strip().split()
        rules[parts[0]] = parts[2]

current_state = deque(init_state)

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

# Get set up
print(''.join(current_state))
potzero_offset = None
gen = 0
print(gen, potzero_offset, potsum(current_state, 0), ''.join(current_state))
next_state, next_offset = nextgen(current_state, potzero_offset)
# Keep going until the state pattern doesn't change anymore
while current_state != next_state:
   gen += 1
   current_state = next_state
   potzero_offset = next_offset
   print(gen, potzero_offset, potsum(current_state, 0), ''.join(current_state))
   next_state, next_offset = nextgen(current_state, potzero_offset)
offset_delta = next_offset - potzero_offset
# display the first repeated state
print(gen, next_offset, potsum(next_state, 0), ''.join(next_state))

print(f'steady state pattern reached at gen {gen}, offset of {potzero_offset} will increase {offset_delta} per future generation')

# fast forward to generation 50000000000
target_gen = 50000000000
ffwd_gens = target_gen - gen
final_offset = potzero_offset + (offset_delta * ffwd_gens)
final_sum = potsum(current_state, final_offset)
print(f'After {target_gen} iterations, the final pot sum will be: {final_sum}')

