"""
# Multicolored lines 
# Original: https://nbviewer.jupyter.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
# References: https://matplotlib.org/stable/gallery/lines_bars_and_markers/multicolored_line.html
# Topics: line, color, LineCollection, cmap, colorline, codex

Defines a function colorline that draws a (multi-)colored 2D line with coordinates x and y.
The color is taken from optional data in z, and creates a LineCollection.

z can be:
- empty, in which case a default coloring will be used based on the position along the input arrays
- a single number, for a uniform color [this can also be accomplished with the usual plt.plot]
- an array of the length of at least the same length as x, to color according to this data
- an array of a smaller length, in which case the colors are repeated along the curve

The function colorline returns the LineCollection created, which can be modified afterwards.

See also: plt.streamplot
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm


# Data manipulation:

def make_segments(x, y):
    """
    Create list of line segments from x and y coordinates, in the correct format for LineCollection:
    an array of the form   numlines x (points per line) x 2 (x and y) array
    """

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    return segments


# Interface to LineCollection:

def colorline(x, y, z=None, cmap=plt.get_cmap('copper'), norm=plt.Normalize(0.0, 1.0), linewidth=3, alpha=1.0):
    """
    Plot a colored line with coordinates x and y
    Optionally specify colors in the array z
    Optionally specify a colormap, a norm function and a line width
    """
    
    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))
           
    # Special case if a single number:
    if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
        z = np.array([z])
        
    z = np.asarray(z)
    
    segments = make_segments(x, y)
    lc = LineCollection(segments, array=z, cmap=cmap, norm=norm, linewidth=linewidth, alpha=alpha)
    
    ax = plt.gca()
    ax.add_collection(lc)
    
    return lc
        
    
def clear_frame(ax=None): 
    # Taken from a post by Tony S Yu
    if ax is None: 
        ax = plt.gca() 
    ax.xaxis.set_visible(False) 
    ax.yaxis.set_visible(False) 
    for spine in ax.spines.itervalues(): 
        spine.set_visible(False) 

## Aditional
def _x(line):
    return np.array([node.x for node in line])
def _y(line):
    return np.array([node.y for node in line])



import multicolored_lines as mcl
from mpl_toolkits.axes_grid1 import make_axes_locatable

#import importlib
#importlib.reload(mcl)

def calculate_new_borders(bounds, margin):
    (minx, maxx, miny, maxy) = bounds

    margin_x = (maxx - minx)*margin/2
    margin_y = (maxy - miny)*margin/2 
    return (minx - margin_x, maxx + margin_x, miny - margin_y, maxy + margin_y)

def gradient_plotlines(output_lines, bounds, nodes, margin = 0.1, **kwargs):

    minx, maxx, miny, maxy = calculate_new_borders(bounds, margin)

    fig, ax = plt.subplots(figsize=(18,18))
    ax.set_facecolor('#111155')
    ax.set_xlim(minx, maxx) 
    ax.set_ylim(miny, maxy)
    ax.set_aspect(1.0)

    #divider = make_axes_locatable(ax)
    #cax = divider.append_axes("right", size="5%", pad=0.05)

    draw_bundled_gradient_edges(output_lines,**kwargs)
    #cb = plt.colorbar(lc)
    #cb.set_alpha(1.)

    plt.scatter(nodes.x, nodes.y, s=12, c='#FFFFFF')
    plt.show()

def draw_bundled_gradient_edges(output_lines, **kwargs):
    for line in output_lines:
        colorline(_x(line),_y(line), **kwargs)