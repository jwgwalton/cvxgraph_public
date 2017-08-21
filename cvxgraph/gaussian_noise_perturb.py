#!/usr/bin/env python3
import numpy as np
from graphs.graph import Graph
sqrt2=1.4142135623730950488016887242

def perturb_matrix(A,sigma):
  e=np.random.normal(scale=sigma,size=A.shape)
 # for i in range(A.shape[0]): e[i,i]=0.0 # having 0 on diagonal ruins covariance matrix
  return A+(e+e.transpose())/sqrt2  # symmetrized


def is_symmetric(matrix):
  tol  = 1e-6
  m,n = matrix.shape
  for i in range(n):
    for j in range(i):
      if abs(matrix[i,j] -matrix[j,i])>tol:
        return False
  return True


if __name__ == '__main__': 
  n=16
  A = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),) 
  A_matrix = Graph.create_adjacency_matrix(n,A)

  A_matrix_noisy = perturb_matrix(A_matrix,0.4)


  print(is_symmetric(A_matrix_noisy)) 
