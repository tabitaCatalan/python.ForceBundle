# Test of updating edge subdivisions 

import unittest
import ForcedirectedEdgeBundling as feb
#import update_subdiv_temp as feb
from numba.typed import List
from numba.types import ListType
from numba.experimental import jitclass
import math

class TestSubDiv(unittest.TestCase):
    def are_equal(self, a, b):
        return math.isclose(a.x, b.x) and math.isclose(a.y, b.y)
    def suma(self, a, b):
        return feb.Point(a.x + b.x, a.y + b.y)
    def resta(self, a, b):
        return self.suma(a, self.pond(-1., b))
    def norma(self, point):
        return math.sqrt(math.pow(point.x,2) + math.pow(point.y,2))
    def distancia(self, a, b):
        return self.norma(self.resta(a, b))

    def pond(self, escalar, point):
        return feb.Point(escalar * point.x, escalar * point.y)
    
    def calculate_point_at_distance(self, point, distance, x):
        p_y = math.sqrt(math.pow(distance,2) - math.pow(x - point.x, 2)) + point.y
        return p_y


    def setUp(self):
        aux1 = feb.Point(2.,1.)
        aux2 = feb.Point(0.5,0.)

        a = feb.Point(0.0, 0.0)
        b = self.suma(a, self.pond(2.5, aux1)) # feb.Point(2.5 * aux1.x,  2.5 * aux1.y) 
        c = self.suma(b, aux2) #feb.Point( b.x + aux2.x,  b.x + aux2.y)

        d_x = 7.0
        d_y = self.calculate_point_at_distance(c, 4 * math.sqrt(5) - self.distancia(a,b) - self.distancia(b, c), d_x)
        d = feb.Point(d_x, d_y)
        print(f"d = ({d.x, d.y})")

        
        ## Save variables 
        self.a, self.b, self.c, self.d = a, b, c, d
        self.aux1, self.aux2 = aux1, aux2 

        # Calculate updated point
        subdivision_points = List()
        #subdivision_points = []
        subdivision_points.append(a)
        subdivision_points.append(b)
        subdivision_points.append(c)
        subdivision_points.append(d)
        subdiv_list = List()
        #subdiv_list = []
        subdiv_list.append(subdivision_points)
        self.subdiv_list = subdiv_list

        # TODO encontrar una mejor manera plis, es grosero
        # si no se usa una copia se modifica el original 
        # y test_initial_length se cae
        subdivision_points_copy = List()
        #subdivision_points_copy = []

        subdivision_points_copy.append(a)
        subdivision_points_copy.append(b)
        subdivision_points_copy.append(c)
        subdivision_points_copy.append(d)
        subdiv_list_copy = List()
        #subdiv_list_copy = []
        subdiv_list_copy.append(subdivision_points)

        edge = feb.Edge(a, d)
        edge_list = List()
        #edge_list = []
        edge_list.append(edge)
        self.updated_points = feb.update_edge_divisions(edge_list, subdiv_list_copy, 3)
        pass

    
    def test_source(self):
        self.assertTrue(self.are_equal(self.a, self.updated_points[0][0]))
        
    def test_inner_nodes(self):
        # node 1
        point1 = self.aux1 
        
        # node 2
        point2 = self.suma(self.a, self.pond(2., self.aux1))
        
        # node 3
        c_d = self.resta(self.c,self.d)
        aux = self.pond(math.sqrt(5)/ self.norma(c_d), c_d)
        point3 = self.suma(self.d, aux)   

        pass

        # asserts
        self.assertTrue(self.are_equal(self.aux1, self.updated_points[0][1]))
        self.assertTrue(self.are_equal(point2, self.updated_points[0][2]))
        self.assertTrue(self.are_equal(point3, self.updated_points[0][3]))

    def test_target(self):
        self.assertTrue(self.are_equal(self.d, self.updated_points[0][-1]))
    
    def test_initial_length(self):
        pass
        self.assertEqual(feb.compute_divided_edge_length(self.subdiv_list, 0), 4. * math.sqrt(5))
        
        
if __name__ == '__main__':
    unittest.main()