#!/usr/bin/env python3
from graphs.graph import Graph

class Utils():
  def __init__():
    pass

  @staticmethod
  def deep_equals(A,B):
    '''
    check equality of symmetric matrices
    Args:
     A (matrix) 
     B (matrix)

    Returns
     bool, true if A_ij == B_ij
    '''
    m,n = A.shape # does this only work on numpy matrices?
    for i in range(0,n):
      for j in range(0,i):
        if(A[i,j] != B[i,j]):
          return False
    return True

if __name__ == '__main__':

  # Test deep_equals works

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

  result = Utils.deep_equals(A_matrix, A1_matrix+A2_matrix)

  print('A=A1+A2: ',result)

