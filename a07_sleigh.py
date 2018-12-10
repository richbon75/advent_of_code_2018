from collections import defaultdict
from heapq import heappop, heappush, heapify

# relates steps to the steps they unblock
instructions = defaultdict(list)
# relates steps to the steps they are blocked by
blocked_by = defaultdict(set)
all_steps = set()

with open('a07_input.txt', 'r') as f:
    for line in f:
        from_step = line[5]
        to_step = line[36]
        instructions[from_step].append(to_step)
        blocked_by[to_step].add(from_step)
        all_steps.add(from_step)
        all_steps.add(to_step)

pending_steps = list(all_steps.difference(blocked_by))
heapify(pending_steps)

visited = []

while pending_steps:
    on_step = heappop(pending_steps)
    visited.append(on_step)
    for unblocked in instructions[on_step]:
        blocked_by[unblocked].remove(on_step)
        if not blocked_by[unblocked]:
            heappush(pending_steps, unblocked)

print(f"Visited in this order: {''.join(visited)}")










