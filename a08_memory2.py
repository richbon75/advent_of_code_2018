
data = ''

with open('a08_input.txt', 'r') as f:
    for line in f:
        data = line

data = [int(x) for x in data.strip().split()]

metadatasum = 0

def visit(data, startpos, depth):
    # print(f'depth = {depth}')
    children = data[startpos]
    metadata_len = data[startpos+1]
    current_pos = startpos+2
    child = 0
    childvalues = [0] * children
    while child < children:
        current_pos, childvalue = visit(data, current_pos, depth+1)
        childvalues[child] = childvalue
        child += 1
    metadata = data[current_pos:current_pos+metadata_len]
    global metadatasum
    metadatasum += sum(metadata)
    ## Determine this node's value
    if children == 0:
        nodevalue = sum(metadata)
    else:
        # NOTE: a metadata value of 1 means "the first element"
        # so it corresponds to an index value of 0
        nodevalue = sum([childvalues[x-1] for x in metadata if (x < children+1 and x > 0)])
    current_pos = current_pos+metadata_len
    return current_pos, nodevalue

current_pos = 0
outpos, rootvalue = visit(data, current_pos, 0)

print(f'Metadata sum: {metadatasum}')
print(f'Root node value: {rootvalue}')

