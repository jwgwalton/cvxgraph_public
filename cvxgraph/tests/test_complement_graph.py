import numpy.testing as npt
import numpy as np
import unittest

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'graphs'))
from complement_graph import ComplementGraph

class TestComplementGraph(unittest.TestCase):
 
  def setUp(self):
    self.n=4
    self.K_4_list=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3),)
    self.K_4_complement_list=()

  def test_k4_iterator(self): 
    iterator  = ComplementGraph.iterator(self.n,self.K_4_list)
    self.assertEquals(tuple(iterator), self.K_4_complement_list)

  def test_empty_iterator(self): 
    iterator  = ComplementGraph.iterator(self.n,self.K_4_complement_list)
    self.assertEquals(tuple(iterator), self.K_4_list)

#  def test_k4_generator(self): 
 #   empty_list_generator  = ComplementGraph.generator(self.n,self.K_4_list)
  #  self.assertEquals(empty_list_generator, self.K_4_complement_list)

  #def test_empty_generator(self): 
   # generator  = ComplementGraph.generator(self.n,self.K_4_complement_list)
    #self.assertEquals(generator, self.K_4_list)

if __name__ == '__main__':
    unittest.main()
