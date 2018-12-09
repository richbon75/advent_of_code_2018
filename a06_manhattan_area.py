'''If the area is bounded by the edge of the outermost points,
any point that has a "closest" block appearing on the edge
of that space effectively has an infinite area, and is discounted.'''

import math
from collections import Counter

points = []
with open('a06_input.txt', 'r') as f:
    for line in f:
        points.append(tuple([int(x) for x in line.strip().split(',')]))

# find the border that encloses these points,
# this defines our whole search area.
top = min([point[0] for point in points]) 
bottom = max([point[0] for point in points]) 
left = min([point[1] for point in points]) 
right = max([point[1] for point in points]) 

def mdist(x1, y1, x2, y2):
    # return the manhattan distance between two points
    return abs(x1-x2) + abs(y1-y2)

def closest_point(points, x, y):
    # given a list of points, find the index of the point
    # with the shortest manhattan distance to (x, y)
    closest_index = None
    closest_distance = math.inf  # infinity
    tie = False
    for i, point in enumerate(points):
        dist = mdist(x, y, *point)
        if dist < closest_distance:
            closest_distance = dist
            closest_index = i
            tie = False
            continue
        if closest_distance == dist:
            # We've found a tie, so unless we find something yet shorter,
            # we can't use it.
            tie = True
    if tie:
        return None
    return closest_index

areas = Counter()
infinite_areas = set()
for i in range(top, bottom+1):
    for j in range(left, right+1):
        closest_index = closest_point(points, i, j)
        if closest_index is not None:
            areas[closest_index] += 1
            if i == top or i == bottom or j == left or j == right:
                infinite_areas.add(closest_index)

non_infinite_in_descending_order_of_area = (
    sorted([x for x in areas.items() if x[0] not in infinite_areas], key = lambda x:x[1], reverse=True))

print(f'Area of largest non-infinite area: {non_infinite_in_descending_order_of_area[0][1]}')
