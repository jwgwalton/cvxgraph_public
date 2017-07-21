import unittest

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', ))
from graphs.graph import Graph
from utils.utils import Utils

class TestUtils(unittest.TestCase):

  def setUp(self):
    self.n = 4
    # A= K_4
    self.A = ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3),)
    # A1 = cycle 
    self.A1 = ((0,1),(1,2),(2,3),(3,0),)
    # A2 = cross joining all nodes
    self.A2=((0,2),(1,3),)

  def test_deep_equals(self):
    A_matrix  = Graph.create_adjacency_matrix(self.n,self.A)
    A1_matrix  = Graph.create_adjacency_matrix(self.n,self.A1)
    A2_matrix  = Graph.create_adjacency_matrix(self.n,self.A2)

    result = Utils.deep_equals(A_matrix, A1_matrix+A2_matrix, 1e-4)
    self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
