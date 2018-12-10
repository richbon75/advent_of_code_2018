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

class Worker(object):

    def __init__(self, pending_steps, instructions, blocked_by, visited, all_steps):
        self.pending_steps = pending_steps
        self.instructions = instructions
        self.blocked_by = blocked_by
        self.visited = visited
        self.all_steps = all_steps
        self.on_step = None
        self.time_left = 0
    
    def pick_up(self):
        if not self.time_left and pending_steps:
            self.on_step = heappop(pending_steps)
            self.time_left = 60 + (ord(self.on_step)-64)

    def work(self):
        if self.time_left > 0:
            self.time_left -= 1
            if not self.time_left:
                self.complete_step()

    def complete_step(self):
        self.visited.append(self.on_step)
        self.all_steps.remove(self.on_step)
        for unblocked in self.instructions[self.on_step]:
            self.blocked_by[unblocked].remove(self.on_step)
            if not self.blocked_by[unblocked]:
                heappush(self.pending_steps, unblocked)
        self.on_step = None

workers = []
for i in range(0, 5):
    workers.append(Worker(pending_steps, instructions, blocked_by, visited, all_steps))

seconds = 0
while all_steps:
    for worker in workers:
        worker.pick_up()
    for worker in workers:
        worker.work()
    seconds += 1

print(f"Visited in this order: {''.join(visited)}")
print(f"Took this many seconds: {seconds}")










