'''
  . open ground
  | trees
  # lumberyard

'''
from collections import Counter

ground = dict()
maxy = -float('inf')
maxx = -float('inf')

with open('a18_input.txt', 'r') as f:
    y = -1
    for line in f:
        y+=1
        x=0
        line = line.strip()
        for x, char in enumerate(line):
            ground[(x,y)] = char
            maxy = max(maxy,y)
            maxx = max(maxx,x)

def surrounding_pos(ground, pos):
    'Given a position, return the surrounding positions'
    return  [(dx + pos[0], dy + pos[1]) for 
                dx, dy in ((-1,-1,),(0,-1),(1,-1),
                            (-1, 0),        (1, 0),
                            (-1, 1), (0, 1),(1, 1))
                if ((dx + pos[0]) >= 0 and (dx + pos[0]) <= maxx and
                    (dy + pos[1]) >= 0 and (dy + pos[1]) <= maxy)]

def whatsaround(ground, pos):
    w = Counter((ground[xy] for xy in surrounding_pos(ground, pos)))
    return w

def newthing(ground, pos):
    w = whatsaround(ground, pos)
    if ground[pos] == '.' and w['|'] >= 3:
        return '|'
    if ground[pos] == '|' and w['#'] >= 3:
        return '#'
    if ground[pos] == '#' and (w['#'] == 0 or w['|'] == 0):
        return '.'
    return ground[pos]

def minute(ground):
    nextground = dict()
    for pos in ground:
        nextground[pos] = newthing(ground, pos)
    return nextground

def resource(ground):
    c = Counter([g for g in ground.values()])
    # print(c, f"Resource value: {c['|'] * c['#']}")
    return c['|'] * c['#']

def gprint(ground):
    for y in range(0, maxy+1):
        outline = []
        for x in range(0, maxx+1):
            outline.append(ground.get((x,y), 'x'))
        print(''.join(outline))

gprint(ground)
last_resource = 0
outfile = open('a18_output.txt', 'w')
for m in range(1,1000):
    # print(f'\n\nMinute: {m}')
    ground = minute(ground)
    # gprint(ground)
    this_resource = resource(ground)
    outfile.write(f'{m} {this_resource}\n')
    last_resource = this_resource
outfile.close()
print('all done')

# In looking at my resulting output file, it eventually settles to a 28-element cycle
'''
min resource
900 188760
901 189945
902 183464
903 181930
904 176080
905 177660
906 173240
907 175150
908 173545
909 176280
910 173545
911 176648
912 177057
913 181068
914 181853
915 187726
916 190836
917 196392
918 198830
919 202410
920 205686
921 205674
922 201718
923 200208
924 195640
925 195026
926 190740
927 193336
928 188760
'''
#  (1000000000 - 900) % 28 = 16 => 916 = 190836


