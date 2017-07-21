import numpy as np
import unittest

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lovasz_calculator import LovaszCalculator
from graphs.graph import Graph

class TestLovaszCalculator(unittest.TestCase):
 
  def setUp(self):
    self.calculator=LovaszCalculator()
    self.n_K3 = 3
    self.K3 = ((0,1),(0,2),(1,2),)

    self.n_K4 = 4
    self.K4 = ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3),)

  def test_lovasz_lambda_k3(self): 
    status,value = self.calculator.calculate(self.n_K3, self.K3, method=self.calculator.LAMBDA_METHOD)

    self.assertEquals(status, 'optimal')
    self.assertAlmostEqual(value, 1)

  def test_lovasz_lambda_k4(self): 
    status,value = self.calculator.calculate(self.n_K4, self.K4, method=self.calculator.LAMBDA_METHOD)

    self.assertEquals(status, 'optimal')
    self.assertAlmostEqual(value, 1)

  def test_lovasz_trace_k3(self): 
    status,value = self.calculator.calculate(self.n_K3, self.K3, method=self.calculator.TRACE_METHOD)

    self.assertEquals(status, 'optimal')
    self.assertAlmostEqual(value, 1)

  def test_lovasz_trace_k4(self): 
    status,value = self.calculator.calculate(self.n_K4, self.K4, method=self.calculator.TRACE_METHOD)

    self.assertEquals(status, 'optimal')
    self.assertAlmostEqual(value, 1)

if __name__ == '__main__':
    unittest.main()
