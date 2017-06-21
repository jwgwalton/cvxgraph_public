#!/usr/bin/env python3
import cvxpy as cvx
import numpy as np
from deconvolve import create_adjacency_matrix
from constraints.spectral_hull_constraint import SpectralHullConstraint

def test_family(A, M, constraints):

  objective = cvx.Maximize(cvx.trace(A*M))

  problem = cvx.Problem(objective,constraints)
  problem.solve()

  if problem.status=='optimal':
    return problem.value
  else:
    return np.nan


def generate_cycle_family_constraints(n,M,A):
  # set of cycles on 16 nodes

  # all values between 0 and 1
  limit_constraints = [M>=0,M<=1] 

  # diag(A) == 0
  diagonal_constraints =[]
  for i in range(n):
    diagonal_constraints.append(M[i,i]==0)    

  # all nodes have degree 2
  one_vec=np.ones(n)
  degree_constraints = [(1/2)*M*one_vec == one_vec]

  # TODO weird convex graph invariant

  spectral_hull_constraint = SpectralHullConstraint(A,M)

  return limit_constraints + diagonal_constraints + degree_constraints + spectral_hull_constraint.constraint_list



def generate_sparse_well_connected_constraints(n,M,A):
  # sparse well-connected graphs on 16 nodes

  # all values between 0 and 1
  limit_constraints = [M>=0,M<=1]

  # diag(M) == 0
  diagonal_constraints =[]
  for i in range(n):
    diagonal_constraints.append(M[i,i]==0)    

  # (A*ones)_i <= 2.5
  one_vec=np.ones(n)
  degree_constraints = [M*one_vec <= 2.5]

  # TODO 2nd smalled eigenvalue of the laplacian must be >= 1.1


  return limit_constraints + diagonal_constraints + degree_constraints

  

if __name__ == '__main__':
  # a 16 cycle
  n =16
  A = ((0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10),(10,11),(11,12),(12,13),(13,14),(14,15),(15,0))
  A_matrix = create_adjacency_matrix(n,A)

  M = cvx.Symmetric(n)

  family_1_constraints = generate_cycle_family_constraints(n,M,A_matrix)
  family_2_constraints = generate_sparse_well_connected_constraints(n,M,A_matrix)

  family_1_similarity = test_family(A_matrix, M, family_1_constraints)
  family_2_similarity = test_family(A_matrix, M, family_2_constraints)

  print('First family similarity: ',family_1_similarity)
  print('Second family similarity: ',family_2_similarity)

  if family_1_similarity >= family_2_similarity:
    print('The first family is the best match for the graph')
  else:
    print('The second family is the best match for the graph')
