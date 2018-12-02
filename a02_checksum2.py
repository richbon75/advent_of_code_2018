def compare(first, second):
    '''determine if two words differ by a single letter
    if so, return the common characters
    else, return empty string'''
    assert len(first) == len(second)
    skips = 0
    common = []
    for i in range(0, len(first)):
        if first[i] == second[i]:
            common.append(first[i])
        else:
            skips += 1
        if skips > 1:
            return ''
    return ''.join(common)

def find_oneoff(codes):
    '''iterate through the list of codes and compare them'''
    for i in range(0, len(codes)):
        for j in range(i+1, len(codes)):
            result = compare(codes[i], codes[j])
            if result:
                return result
    return 'Nothing found'

# read the codes into a list and operate on that
codes = []
f = open('a02_input.txt', 'r')
for line in f:
    value = line.strip()
    codes.append(value)
f.close()

# find the answer
print(find_oneoff(codes))

