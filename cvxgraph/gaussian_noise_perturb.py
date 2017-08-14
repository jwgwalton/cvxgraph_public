#!/usr/bin/env python3
import numpy as np
from graphs.graph import Graph


def perturb_matrix(n,matrix, perturbation_scale):
  perturbation_matrix = np.random.normal(scale=perturbation_scale,size=(n,n))
  perturbation_matrix += perturbation_matrix.T
  perturbation_matrix = 0.5*perturbation_matrix
  return matrix+perturbation_matrix


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

  A_matrix_noisy = perturb_matrix(n,A_matrix,0.4)


  print(is_symmetric(A_matrix_noisy))
