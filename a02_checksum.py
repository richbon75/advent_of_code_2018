
def analyze(value):
    '''analyze a value and determine if it has characters
    that appear 2 times and/or characters that appear 3 times'''
    # get counts of letters
    counts = dict()
    for letter in value:
        counts[letter] = counts.get(letter, 0) + 1
    # check for appearance counts of 2 or 3
    two = three = 0
    for key, value in counts.items():
        if value == 2:
            two = 1
        elif value == 3:
            three = 1
    return two, three

sum2 = sum3 = 0
f = open('a02_input.txt', 'r')
for line in f:
    value = line.strip()
    two, three = analyze(value)
    sum2 += two
    sum3 += three
f.close()

print(f'Answer = {sum2 * sum3}') 

