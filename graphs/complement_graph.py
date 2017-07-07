#!/usr/bin/env python3
import numpy as np
from itertools import product

class ComplementGraph():

  @staticmethod
  def iterator(n,edge_list):
    '''
    iterator for generating the complement of a graph from its edge list

    params
    n: dimensions of adjacency matrix
    edge_list: list or tuple of tuples of edge coordinates
           (assumes symmetry of adjacency matrix so only edges in upper diagonal area)

    returns tuple of coordinates of i~j not in E

    Complement of graph, full list of all edges which do not exist in initial graph
  '''
    for i,j in product(range(n),repeat=2):
      if i == j: continue 
      if (i,j) not in edge_list and (j,i) not in edge_list:
        yield (i,j)

  @staticmethod
  def generator():
    # FIXME use generator from lovasz_number/graph_utils
    return []
