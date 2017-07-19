#!/usr/bin/env python3
from graphs.graph import Graph
import numpy.testing as npt
import numpy as np
import unittest

class TestGraph(unittest.TestCase):
 
  def setUp(self):
    self.n=4
    self.K_4_list=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3),)
    self.K_4_matrix=np.matrix('0 1 1 1; 1 0 1 1; 1 1 0 1; 1 1 1 0')

  def test_create_adjacency_matrix(self): 
    matrix  = Graph.create_adjacency_matrix(self.n,self.K_4_list)
    npt.assert_array_equal(matrix, self.K_4_matrix)

  def test_create_adjacency_list(self): 
    adjacency_list  = Graph.create_adjacency_list(self.n,self.K_4_matrix)
    self.assertEquals(adjacency_list, self.K_4_list)
  
  def test_instantiate_graph_with_list(self):
    graph = Graph(self.n, adjacency_list=self.K_4_list)
    self.assertEquals(graph.adjacency_list, self.K_4_list)
    npt.assert_array_equal(graph.adjacency_matrix, self.K_4_matrix)

  def test_instantiate_graph_with_matrix(self):
    graph = Graph(self.n, adjacency_matrix=self.K_4_matrix)
    self.assertEquals(graph.adjacency_list, self.K_4_list)
    npt.assert_array_equal(graph.adjacency_matrix, self.K_4_matrix)

  def test_instantiate_graph_empty_list(self):
    graph = Graph(self.n,adjacency_list=())
    self.assertEquals(graph.adjacency_list, ())
    npt.assert_array_equal(graph.adjacency_matrix, np.zeros((self.n,self.n)))

  def test_instantiate_empty_graph_throws_error(self):
    with self.assertRaises(ValueError) as exception:
      graph = Graph(self.n)
    self.assertTrue('Pass in adjacency list or adjacency matrix to instantiate Graph object', exception)

if __name__ == '__main__':
    unittest.main()
