#!/usr/bin/env python3
import cvxpy as cvx
import numpy as np
from constraints.spectral_hull_constraint import SpectralHullConstraint
from constraints.node_limit_constraint import NodeLimitConstraint
from graphs.graph import Graph


def check_solution(A1,A2, tol):
  '''
  Checks returns exact decomposition, i.e returns integers for the distinct edges
  '''
  m,n = A1.shape
  convolved_matrix = A1 + A2
  for i in range(1,n):
    for j in range(1,i):
     if convolved_matrix[i,j] < 1+tol or convolved_matrix[i,j] > 0+tol:
       return False
  return True

def deconvolve(n,A_matrix,A1_matrix,A2_matrix):
  '''
  n: number of nodes/dimension of adjacency matrix
  A: Composition of A1 and A2
  A1: Component of A 
  A2: component of A
  '''

  # Realisations of the precise labelling of A1 and A2
  A1_labelled = cvx.Symmetric(n)  
  A2_labelled = cvx.Symmetric(n)

  # objective function
  objective = cvx.Minimize(cvx.pnorm((A_matrix - A1_labelled - A2_labelled), 2))

  # Constraint sets
  A1_hull = SpectralHullConstraint(A1_matrix, A1_labelled)
  A2_hull = SpectralHullConstraint(A2_matrix, A2_labelled)

  # all values between 0 and 1
  A1_limits = NodeLimitConstraint(A1_labelled,lower_limit=0, upper_limit=1)
  A2_limits = NodeLimitConstraint(A2_labelled,lower_limit=0, upper_limit=1)

  constraints = A1_hull.constraint_list + A2_hull.constraint_list + A1_limits.constraint_list + A2_limits.constraint_list 

  problem = cvx.Problem(objective,constraints)

  problem.solve(kktsolver='robust')

  # TODO check correctness by looking at intersection of tangent cones for A1_labelled and A2_labelled
  # correct if and only if
  #  Tc(A1_labelled) ∩ - Tc(A2_labelled) ={0}

  # checks if within tolerance of 0 and 1
  problem_correct = check_solution(A1_labelled.value, A2_labelled.value, 1e-4)
  print('Problem correct: ', problem_correct)

  if problem.status=='optimal':
    return problem.status,problem_correct,problem.value,A1_labelled.value,A2_labelled.value
  else:
    return problem.status,problem_correct,np.nan,np.nan,np.nan


if __name__ == '__main__':
  # complete graph, K_4, not appropriate for deconvolve?

  # A= K_4
  n = 4
  A=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3),)

  # A1 = cycle 
  A1=((0,1),(1,2),(2,3),(3,0),)

  # A2 = cross joining all nodes
  A2=((0,2),(1,3),)

  A_matrix  = Graph.create_adjacency_matrix(n,A)
  A1_matrix = Graph.create_adjacency_matrix(n,A1)
  A2_matrix = Graph.create_adjacency_matrix(n,A2)

  status,is_correct,problem_value,A1_star,A2_star= deconvolve(n,A_matrix,A1_matrix,A2_matrix)

  np.set_printoptions(suppress=True)
  print('Problem status: ',status)
  print('Norm value: ',problem_value)
  print('A:  \n', A_matrix)
  print('A1: \n', A1_star)
  print('A2: \n', A2_star)
  print('A1+A2: \n ', np.add(A1_star,A2_star))

