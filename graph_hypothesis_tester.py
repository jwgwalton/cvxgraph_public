#!/usr/bin/env python3
import cvxpy as cvx
import numpy as np
from deconvolve import create_adjacency_matrix

def test_family(n,A, family_constraint)

  np.random.seed(1)
  M = np.random.normal(size=(n,n))

  objective = cvx.Maximize(cvx.trace(A*M))

  problem = cvx.Problem(objective,constraints)
  problem.solve()

  # do i return the problem value to compare?, can trim this down i think
  if problem.status=='optimal':
    return problem.value
  else:
    return np.nan

def test_hypothesis(n, A, family_1_constraints, family_2_constraints):

  np.random.seed(1)
  M = np.random.normal(size=(n,n))

  family_1_similarity = test_family(n, A, family_1_constraints)
  family_2_similarity = test_family(n, A, family_2_constraints)
  
  return family_1_similarity > family_2_similarity

def generate_cycle_family_constraints(n,A):
  # set of cycles on 16 nodes

  # all values between 0 and 1
  limit_constraints = [A>=0,A<=1] 

  # diag(A) == 0
  diagonal_constraints =[]
  for i in range(n):
    diagonal_constraints.append(A[i,i]==0)    

  # all nodes have degree 2
  one_vec=np.ones(n)
  degree_constraints = [(1/2)*A*one_vec == one_vec]

  # TODO weird convex graph invariant

  # TODO spectrum of a cycle



def generate_sparse_well_connected_constraints(n,A):
  # sparse well-connected graphs on 16 nodes

  # all values between 0 and 1
  limit_constraints = [A>=0,A<=1]

  # diag(A) == 0
  diagonal_constraints =[]
  for i in range(n):
    diagonal_constraints.append(A[i,i]==0)    

  # (A*ones)_i <= 2.5
  one_vec=np.ones(n)
  degree_constraints = [A*one <= 2.5]

  # TODO 2nd smalled eigenvalue of the laplacian must be >= 1.1

  

if __name__ == '__main__':
  # a 16 cycle
  n =16
  A = ((0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10),(10,11),(11,12),(12,13),(13,14),(14,15),(15,0))
  A_matrix = create_adjacency_matrix(n,A)

  family_1_constraints = generate_cycle_family_constraints(n,A_matrix)
  family_2_constraints = generate_sparse_well_connected_constraints(n,A_matrix)

  result = test_hypothesis(n, A_matrix, family_1_constraints, family_2_constraints)

  print('The first family is the best match for the graph: ', result)

