import re

'''This is a variation on the solution that uses a Set to track
the overlapped squares and does NOT create a full matrix of
the fabric in memory.'''

regex = r"^#(?P<code>\d+) @ (?P<col>\d+),(?P<row>\d+): (?P<width>\d+)x(?P<height>\d+)"
swatches = []
overlaps = set()
freecode = None

f = open('a03_input.txt', 'r')
for line in f:
    m = re.match(regex, line.strip()).groupdict()
    swatches.append(
        {"code": int(m['code']),
         "row_from": int(m['row']),
         "row_to": int(m['row']) + int(m['height']) -1,
         "col_from": int(m['col']),
         "col_to": int(m['col']) + int(m['width']) - 1
        }
    )
f.close()

for i in range(0, len(swatches)):
    for j in range(i+1, len(swatches)):
        overlap_start = (max(swatches[i]['row_from'], swatches[j]['row_from']),
                         max(swatches[i]['col_from'], swatches[j]['col_from']))
        overlap_stop = (min(swatches[i]['row_to'], swatches[j]['row_to']),
                        min(swatches[i]['col_to'], swatches[j]['col_to']))
        # generate coordinates of any overlapped square inches
        for ii in range(overlap_start[0], overlap_stop[0] + 1):
            for jj in range(overlap_start[1], overlap_stop[1] + 1):
                overlaps.add((ii,jj))

print(f'Overlapping square inches: {len(overlaps)}')

# Cycle through the swatches again to find one that was not overlapped
for i in range(0, len(swatches)):
    overlapped = False
    for ii in range(swatches[i]['row_from'], swatches[i]['row_to']+1):
        if overlapped:
            break
        for jj in range(swatches[i]['col_from'], swatches[i]['col_to']+1):
            if (ii, jj) in overlaps:
                overlapped = True
                break
    if not overlapped:
        freecode = swatches[i]['code']
        break

print(f'Unoverlapped swatch: {freecode}')
