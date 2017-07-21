import numpy as np
import unittest

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from deconvolve import GraphDeconvolver # might not find this
from graphs.graph import Graph

class TestGraphDeconvolver(unittest.TestCase):
 
  def setUp(self):
    self.n=4
    self.A=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3),)
    self.A1=((0,1),(1,2),(2,3),(3,0),)
    self.A2=((0,2),(1,3),)
    self.pertubation_matrix= 0.1*np.ones((self.n,self.n))
    self.tolerance = 0.1

  def test_solution_checker(self): 
    A_matrix  = Graph.create_adjacency_matrix(self.n,self.A)
    A1_matrix = Graph.create_adjacency_matrix(self.n,self.A1)
    A2_matrix = Graph.create_adjacency_matrix(self.n,self.A2)

    perturbed_A1 = A1_matrix - self.pertubation_matrix
    perturbed_A2 = A2_matrix + self.pertubation_matrix
    
    graph_deconvolver = GraphDeconvolver(self.n,self.A1,self.A2)

    result = graph_deconvolver.check_solution(A_matrix,perturbed_A1,perturbed_A2,self.tolerance)

    self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
