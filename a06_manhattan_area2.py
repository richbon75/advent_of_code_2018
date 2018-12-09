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

# For part 2, we're looking for the area made up of coordinates
# that are less than max_sum_dist away from ALL of the points
max_sum_dist = 10000

def mdist(x1, y1, x2, y2):
    # return the manhattan distance between two points
    return abs(x1-x2) + abs(y1-y2)

def closest_point(points, x, y):
    # given a list of points, find the index of the point
    # with the shortest manhattan distance to (x, y)
    # Part 2: modified to also return total distances to all points
    # returns tuple: (closest_index, total distance to all points)
    closest_index = None
    closest_distance = math.inf  # infinity
    tie = False
    total_dist_to_all_points = 0
    for i, point in enumerate(points):
        dist = mdist(x, y, *point)
        total_dist_to_all_points += dist
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
        return None, total_dist_to_all_points
    return closest_index, total_dist_to_all_points

areas = Counter()
infinite_areas = set()
area_within_max_sum_dist = 0
for i in range(top, bottom+1):
    for j in range(left, right+1):
        closest_index, total_dist = closest_point(points, i, j)
        if total_dist < max_sum_dist:
            area_within_max_sum_dist += 1
        if closest_index is not None:
            areas[closest_index] += 1
            if i == top or i == bottom or j == left or j == right:
                infinite_areas.add(closest_index)

non_infinite_in_descending_order_of_area = (
    sorted([x for x in areas.items() if x[0] not in infinite_areas], key = lambda x:x[1], reverse=True))

print(f'Area of largest non-infinite area: {non_infinite_in_descending_order_of_area[0][1]}')

### PART 2
print(f'Area of region containing all locations within max distance: {area_within_max_sum_dist}')


