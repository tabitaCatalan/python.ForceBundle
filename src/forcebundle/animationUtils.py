"""
This file contains the function construct_animation, which can be used
to create an animation of the bundling process.

Base on Vera Sativa's codes
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib

def get_nodes(evolution):
    """Get nodes of the edges from the first iteration
    Return two list with x and y coordinates of nodes
    """
    points_x = []
    points_y = []
    for line in evolution[0][2]:
        for point_key in [0, 2]:
            points_x.append(line[0][point_key])
            points_y.append(line[1][point_key])
    return points_x, points_y

def construct_animation(evolution, bounds, extra_frac = 0.05, alpha = .115):
    """Make an animation of the bundling process
    Arguments:
    evolution -- list of information per iteration. For each iteration in evolution, 
        - iteration[0] correspond to the cycle
        - iteration[1] to the number of the iteration in that cycle
        - iteration[2]: lines of the edges after that iteration
    bounds -- tuple (minx, maxx, miny, maxy). Defines the limits of a box
        that contains al the edges (previous to bundling)
    extra_frac -- number in [0., 1.] percentage added to the box size
    alpha -- transparency of edges (0.0 is totally transparent, 1.0 not transparent)
    
    """

    fig, ax = plt.subplots(figsize=(25, 14))
    fig.set_tight_layout(True)
    ax.set_aspect(1.0)
    anotation = ax.annotate('Cycle: ø | Iteration: ø', (.83, .05), xycoords='axes fraction', color='white')
    nodes_x, nodes_y = get_nodes(evolution)
    ax.scatter(nodes_x, nodes_y, s=10, c='#ffee00')

    lines = []
    for _line_key in range(len(evolution[0][2])):
        lobj = ax.plot([], [], linewidth=1, axes=ax, color='#ff2222', alpha= alpha)[0]
        #lobj = matplotlib.lines.Line2D([], [], linewidth=1, axes=ax, color='#ff2222', alpha=.15)
        lines.append(lobj)


    def animate(frame, evolution):
        for key, line in enumerate(lines):
            line.set_data(evolution[frame][2][key][0], evolution[frame][2][key][1])
        frame_desc = 'Cycle: {} | Iteration: {}'.format(evolution[frame][0], evolution[frame][1])
        anotation.set_text(frame_desc)
        return lines

    def init_plot(bounds, extra_frac, evolution):
        minx, maxx, miny, maxy = bounds 
        extrax = extra_frac * (maxx - minx)
        extray = extra_frac * (maxy - miny)
        #ax.set_ylim(230, 500)
        #ax.set_xlim(-1270, -670)
        ax.set_ylim(miny - extray, maxy + extray)
        ax.set_xlim(minx - extrax, maxx + extrax)
        ax.set_facecolor('#111155')
        ax.axes.get_yaxis().set_visible(False)
        ax.axes.get_xaxis().set_visible(False)
        return animate(0, evolution)


    init = lambda: init_plot(bounds, extra_frac, evolution)

    print('Building animation...')
    ani = FuncAnimation(fig, animate, init_func=init, frames=len(evolution), blit=True, interval=300, repeat=False, fargs = (evolution,))
    print('Animation ready!')
    return ani

if __name__ == "__main__":
    import readDataUtils as rd
    csvfile = 'test_data/toycase.csv'
    edges, bounds = rd.read_edges_from_csv(csvfile)
    evolution = rd.bundle_and_save_evolution(edges)
    ani = construct_animation(evolution, bounds, alpha = 0.8)
    animation_name = 'toy.mp4'
    print(f'Saving animation to {animation_name}...')
    ani.save(animation_name, fps=10, extra_args=['-vcodec', 'libx264'])
    print('Animation saved!')