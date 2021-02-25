"""
This file contains utils functions to extract data from csv files 
and use it to generate lists of edges.

Based on Vera Sativa's codes
"""

import csv 
import forcebundle.ForcedirectedEdgeBundling as feb
import math
from numba import float32, jit, prange, float64, njit
from numba.experimental import jitclass
from numba.typed import List
from numba.types import ListType, int16, uint8
from tqdm.auto import tqdm

#import pickle

def print_edge(edge):
    """A confortable way of displaying an edge"""
    print((edge.source.x, edge.source.y), " --> ", (edge.target.x, edge.target.y))


def _update_bounds(bounds, edge):
    """Expand bounds if source or target of edge is out of them"""
    old_minx, old_maxx, old_miny, old_maxy = bounds
    minx = min(old_minx, edge.source.x)
    minx = min(minx, edge.target.x)
    
    maxx = max(old_maxx, edge.source.x)
    maxx = max(maxx, edge.target.x)
    
    miny = min(old_miny, edge.source.y)
    miny = min(miny, edge.target.y)
    
    maxy = max(old_maxy, edge.source.y)
    maxy = max(maxy, edge.target.y)
    return (minx, maxx, miny, maxy)

transf_function = lambda row: (float(row[0]), float(row[1]), float(row[2]), float(row[3]))

def read_edges_from_csv(csvfilename, transform = transf_function, **kargs):
    """Read a csv file and return a list of edges and limit coordinates.

    Arguments:
    csvfilename -- string pointing to a csv file. Each row correspond
        to an edge, and contains the coordinates of it source and target.
    transform -- function that recieves a row and returns an indexable object
        (tuple, array, list) with transformed data. Default is transform
        everything to float.
    kargs -- other arguments to pass to transform

    Return:
    edges -- list of edges
    bounds -- tuple of four elements: (minx, maxx, miny, maxy), definig
        a box in such a way that every edge is inside. It means that
        minx = min(min_{e in edges} e.source.x, min_{e in edges} e.target.x)
        maxx = max(max_{e in edges} e.source.x, max_{e in edges} e.target.x)
        miny = min(min_{e in edges} e.source.y, min_{e in edges} e.target.y)
        maxy = max(max_{e in edges} e.source.y, max_{e in edges} e.target.y)
        Every edge 

    Example: 
    If csv file contains:
    -4.0, -2.0, -2.0, 3.0 
    -4.0, -4.0, 1.0, 4.0
    a list of two edges will be created ( source --> target):
    (-4.0, -2.0) --> (-2.0, 3.0)
    (-4.0, -4.0) --> (1.0, 4.0)
    """

    with open(csvfilename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        edges = feb.get_empty_edge_list()
        
        bounds = math.inf, 0, math.inf, 0

        for row in csvreader:
            transformed = transform(row)
            source = feb.Point(transformed[0], transformed[1])
            target = feb.Point(transformed[2], transformed[3])
            edge = feb.Edge(source, target)
            edges.append(edge)
            bounds = _update_bounds(bounds, edge)
        
    return edges, bounds 


def bundled_edges2lines(edges):
    lines = []
    for edge in edges:
        linex = []
        liney = []
        for point in edge:
            linex.append(point.x)
            liney.append(point.y)
        lines.append([linex, liney])
    return lines

def bundle_and_save_evolution(edges):
    P = 10 #feb.P_initial        

    subdivision_points_for_edge = feb.build_edge_subdivisions(edges, P)
    compatibility_list_for_edge = feb.compute_compatibility_list(edges)
    subdivision_points_for_edge = feb.update_edge_divisions(edges, subdivision_points_for_edge, P)
    C = 1 #feb.C
    I = 100#feb.I_initial
    S = 0.05 #feb.S_initial

    weights = List.empty_list(float32)
    evolution = []

    for _cycle in tqdm(range(C), unit='cycle'):
        for _iteration in tqdm(range(math.ceil(I)), unit='iteration'):
            forces = List()
            for edge_idx in range(len(edges)):
                forces.append(feb.apply_resulting_forces_on_subdivision_points(edges, subdivision_points_for_edge,
                                                                                compatibility_list_for_edge, edge_idx, feb.K, P,
                                                                                S, weights))
            for edge_idx in range(len(edges)):
                for i in range(P + 1): # We want from 0 to P
                    subdivision_points_for_edge[edge_idx][i] = feb.Point(
                        subdivision_points_for_edge[edge_idx][i].x + forces[edge_idx][i].x,
                        subdivision_points_for_edge[edge_idx][i].y + forces[edge_idx][i].y
                    )
            # Save iteration status
            evolution.append([_cycle, _iteration, bundled_edges2lines(subdivision_points_for_edge)])

        # prepare for next cycle
        S = S / 2
        P = P * feb.P_rate
        I = I * feb.I_rate

        subdivision_points_for_edge = feb.update_edge_divisions(edges, subdivision_points_for_edge, P)
        evolution.append([_cycle, 'ued', bundled_edges2lines(subdivision_points_for_edge)])
    return evolution

#def pickle_evolution(evolution, filename = 'evolution.pkl'):
#    with open(filename, 'wb') as f:
#        # Pickle the 'data' dictionary using the highest protocol available.
#        pickle.dump(evolution, f, pickle.HIGHEST_PROTOCOL)

#def read_pickled_evolution(filename):
#    with open(filename, 'rb') as f:
#        # The protocol version used is detected automatically, so we do not
#        # have to specify it.
#        evolution = pickle.load(f)
#    return evolution