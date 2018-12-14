
data = ''

with open('a08_input.txt', 'r') as f:
    for line in f:
        data = line.strip().split()

data = [int(x) for x in data]

metadatasum = 0

def visit(data, startpos, depth):
    # print(f'depth = {depth}')
    children = data[startpos]
    metadata_len = data[startpos+1]
    current_pos = startpos+2
    while children > 0:
        children -= 1
        current_pos = visit(data, current_pos, depth+1)
    metadata = data[current_pos:current_pos+metadata_len]
    global metadatasum
    metadatasum += sum(metadata)
    current_pos = current_pos+metadata_len
    return current_pos


current_pos = 0
visit(data, current_pos, 0)

print(f'Metadata sum: {metadatasum}')

