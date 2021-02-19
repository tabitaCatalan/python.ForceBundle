# Test feb cycle 

import unittest, csv
import ForcedirectedEdgeBundling as feb
import readDataUtils as rd


class TestCycle(unittest.TestCase):
    
    def setUp(self):
        csvfile = 'test_data/toycase.csv'
        edges, bounds = rd.read_edges_from_csv(csvfile)
        self.edges = edges 
        self.bounds = bounds
        self.S = feb.S_initial
        self.I = feb.I_initial
        self.P = feb.P_initial

        self.subdivision_points_for_edge = feb.build_edge_subdivisions(edges, self.P)
        self.compatibility_list_for_edge = feb.compute_compatibility_list(edges)

    
    def test_cycle(self):
        self.subdivision_points_for_edge = feb.update_edge_divisions(self.edges, self.subdivision_points_for_edge, self.P)
        pass

        
if __name__ == '__main__':
    unittest.main()