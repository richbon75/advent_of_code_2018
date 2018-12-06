
class SleepHistory(object):
    def __init__(self):
        self.sleep = [0] * 60

    def slept(self, from_minute, to_minute):
        for minute in range(from_minute, to_minute):
            self.sleep[minute] += 1
    
    def most_slept_minute(self):
        most_slept = 0
        for i in range(0, len(self.sleep)):
            if self.sleep[i] > self.sleep[most_slept]:
                most_slept = i
        return most_slept


class Guard(object):
    def __init__(self, guardId):
        self.guardId = guardId
        self.sleephistory = SleepHistory()
        self.sleeptotal = 0

    def sleep(self, from_minute, to_minute):
        self.sleephistory.slept(from_minute, to_minute)
        self.sleeptotal += to_minute - from_minute

raw_input = []
f = open('a04_input.txt', 'r')
for line in f:
    raw_input.append(line.strip())
f.close()

raw_input.sort()

guards = {}
current_guard = None
asleep_time = None
for line in raw_input:
    if "Guard" in line:
        current_guard = line.split('#')[1].split(' ')[0]
        continue
    if "falls asleep" in line:
        asleep_time = int(line.split(']')[0].split(':')[1])
        continue
    if current_guard not in guards:
        guards[current_guard] = Guard(current_guard)
    awake_time = int(line.split(']')[0].split(':')[1])
    guards[current_guard].sleep(asleep_time, awake_time)

longest_sleeping_guard = sorted(guards.items(), 
    key = lambda x: x[1].sleeptotal, reverse = True)[0][1]

most_slept_minute = longest_sleeping_guard.sleephistory.most_slept_minute()

print(f'Longest sleeping guard: {longest_sleeping_guard.guardId}')
print(f'Most slept minute: {most_slept_minute}')
print(f'Answer to part 1: {int(longest_sleeping_guard.guardId) * most_slept_minute}')
