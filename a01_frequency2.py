f = open('a01_input.txt')
running_sum = 0
frequencies_reached = set()
frequencies_reached.add(running_sum)
values = []
loop = 0
for line in f:
    values.append(int(line.strip()))
f.close()
answer_found = False
while(not answer_found):
    loop += 1
    print(f'On loop: {loop}')
    for value in values:
        running_sum += value
        if running_sum in frequencies_reached:
            print(f'Answer = {running_sum}')
            answer_found = True
            break
        frequencies_reached.add(running_sum)

