f = open('a01_input.txt')
running_sum = 0
for line in f:
    running_sum += int(line.strip())
print(running_sum)
