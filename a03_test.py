import re

regex = r"^#(?P<code>\d+) @ (?P<col>\d+),(?P<row>\d+): (?P<width>\d+)x(?P<height>\d+)"

test_str = "#118 @ 360,971: 13x12"

m = re.match(regex, test_str).groupdict()

print(m['row'])
