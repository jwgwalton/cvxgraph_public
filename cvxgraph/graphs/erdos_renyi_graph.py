import numpy as np
from random import random
from itertools import combinations

class ErdosRenyiGraph():
  # Check that these methods work correctly??

  def __init__(self, n,p):
    self.n = n
    self.p = p


  def iterator(self):
    '''
    Keith Briggs 2017-06-06
  
    Iterator for creating edge list for an Erdos-Renyi graph G~(n,p)
    '''
    return filter(lambda x: random()<p,combinations(range(n),2))

  def generator(self):
    '''
    method for generating erdos-renyi graph

    returns tuple of coordinates of i~j in E
    '''
    return tuple((i,j) for i,j in combinations(range(self.n),2) if random()<self.p)

