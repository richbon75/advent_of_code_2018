'''This version owes a great debt to Nicolas P. Rougier's
implementation of Conway's Game of Life in Python using NumPy and matplotlib.
http://www.labri.fr/perso/nrougier/from-python-to-numpy/index.html#the-game-of-life
http://www.labri.fr/perso/nrougier/from-python-to-numpy/code/game_of_life_numpy.py

Vectorizing the update with NumPy makes it go about 100x faster
than the loop-heavy stock Python version.
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# The original idea was to find specific colors to use, but
# it turned out I liked the colors represented by their ascii values,
# so I've just left it.  Colors must be in the range 1-255.
colors = {
    '.': ord('.'),
    '|': ord('|'),
    '#': ord('#')
}

def loadfile(filename='a18_input.txt'):
    data=[]
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            data.append(list(line))
    data = np.array(data, dtype='c')
    data = np.vectorize(colors.get)(data).astype(dtype=np.uint8)
    return data

def surround(data, value=0):
    '''Surround a 2D matrix with a border of some value all the way around.
    This is done so that the vectorization in cellcount() doesn't break
    at the edges and corners of the dataset.'''
    target_type = data.dtype
    bigger_shape = (data.shape[0]+2, data.shape[1]+2)
    framed = np.full(bigger_shape, value, dtype=target_type)
    framed[1:-1, 1:-1] = data
    return framed

def cellcount(d, c=ord('|')):
    '''Create a matrix that counts the number of times the value
    of interest (c) appears in the surrounding cells.'''
    # note - adding the scalar zero makes the arrays of booleans
    # sum up like zeros and ones.
    N = ((d[0:-2, 0:-2]==c) + 0 + (d[0:-2, 1:-1]==c) + (d[0:-2, 2:]==c) +
         (d[1:-1, 0:-2]==c) +                          (d[1:-1, 2:]==c) +
         (d[2:,   0:-2]==c) +     (d[2:,   1:-1]==c) + (d[2:,   2:]==c))
    return N

def update(*args):
    global data, im
    F = cellcount(data, colors['|'])  # count Forests
    L = cellcount(data, colors['#'])  # count Lumberyards
    D = data[1:-1,1:-1]
    D[...] = np.where(np.logical_and(D==colors['.'], F>=3), colors['|'],
              np.where(np.logical_and(D==colors['|'], L>=3), colors['#'],
                np.where(np.logical_and(D==colors['#'], np.logical_or(F==0, L==0)), colors['.'], D)))
    im.set_data(data)

# This line would load my challenge file
# data = loadfile('a18_input.txt')

# This line generates a random map
data = np.random.choice(list(colors.values()), size=(500,500))

data = surround(data, value=0)

size = np.array(data.shape)
dpi = 80.0
figsize = size[1]/float(dpi), size[0]/float(dpi)
fig = plt.figure(figsize=figsize, dpi=dpi)
fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False)
im = plt.imshow(data, interpolation='nearest')
plt.xticks([]), plt.yticks([])
animation = FuncAnimation(fig, update, interval=1, frames=500, repeat=False)

'''  # Uncomment this to save your animation as a video file.

animation.save('settlers4.mp4', fps=40, dpi=80, bitrate=-1, codec="libx264",
                extra_args=['-pix_fmt', 'yuv420p'],
                metadata={'artist':'Rich Boniface'})
'''

# Comment this out if you're saving the animation above.
plt.show()

