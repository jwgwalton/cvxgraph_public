#!/usr/bin/env python3
from utils import Utils
from graphs.graph import Graph
import unittest

class TestUtils(unittest.TestCase):

  def test_deep_equals(self):
    # A= K_4
    n = 4
    A=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3),)

    # A1 = cycle 
    A1=((0,1),(1,2),(2,3),(3,0),)

    # A2 = cross joining all nodes
    A2=((0,2),(1,3),)

    A_matrix  = Graph.create_adjacency_matrix(n,A)
    A1_matrix  = Graph.create_adjacency_matrix(n,A1)
    A2_matrix  = Graph.create_adjacency_matrix(n,A2)

    result = Utils.deep_equals(A_matrix, A1_matrix+A2_matrix, 1e-4)
    self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
