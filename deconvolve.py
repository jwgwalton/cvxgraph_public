#!/usr/bin/env python3
import cvxpy as cvx
import numpy as np
from spectral_hull_constraint import SpectralHullConstraint

def create_adjacency_matrix(n, edge_list):
  adjacency_matrix = np.zeros((n,n))
  for k in range(len(edge_list)):
    i,j = edge_list[k]
    adjacency_matrix[i][j]=1
    adjacency_matrix[j][i]=1
  return adjacency_matrix

def deconvolve(n,A,A1,A2):
  '''
  n, number of mades/dimension of adjacency matrix
  A: Composition of A1 and A2, don't know labelling
  A1: Component of A
  A2: component of A
  '''
  A_matrix = create_adjacency_matrix(n,A)
  A1_matrix = create_adjacency_matrix(n,A1)
  A2_matrix = create_adjacency_matrix(n,A2)

  # sum of all eigenvalues
  eigenvalues_A1 = sum(np.linalg.eigvalsh(A1_matrix))
  eigenvalues_A2 = sum(np.linalg.eigvalsh(A2_matrix))

  # check sum of n largest eigenvalues
  #print('Sum of k largest eigenvalues, A1:', eigenvalues_A1)
  #print('Sum of k largest eigenvalues, A2:', eigenvalues_A2)

  trace_A1 = cvx.trace(A1_matrix)
  trace_A2 = cvx.trace(A2_matrix)
  #print('Trace A1: ', trace_A1.value)
  #print('Trace A2: ', trace_A2.value)

  # Realisations of the precise labelling of A1 and A2
  A1_labelled = cvx.Symmetric(n)
  A2_labelled = cvx.Symmetric(n)

  # objective function
  objective = cvx.Minimize(cvx.norm(A_matrix - A1_labelled - A2_labelled))

  # Constraint sets - move to use spectral hull constraint once working properly, easier to read procedurally
  convex_hull_A1 = [cvx.trace(A1_labelled) == trace_A1, cvx.lambda_sum_largest(A1_labelled,n) <= eigenvalues_A1]
  convex_hull_A2 = [cvx.trace(A2_labelled) == trace_A2, cvx.lambda_sum_largest(A2_labelled,n) <= eigenvalues_A2]

  #Values have to be either 0 or 1, how to do it???
  limit_constraints = [A1_labelled>=0, A1_labelled<=1, A2_labelled>=0, A2_labelled<=1] 

  #print('Sum of k largest eigenvalues for labelled A1: ',sum(np.linalg.eigvalsh(A1_labelled.value)))

  constraints =  convex_hull_A1 + convex_hull_A2 + limit_constraints

  problem = cvx.Problem(objective,constraints)

  problem.solve(kktsolver='robust')

  #print('Sum of k largest eigenvalues, A1_labelled: ',sum(np.linalg.eigvalsh(A1_labelled.value)))
  #print('Sum of k largest eigenvalues, A2_labelled: ',sum(np.linalg.eigvalsh(A2_labelled.value)))
  #print('Trace A1_labelled: ', cvx.trace(A1_labelled).value)
  #print('Trace A2_labelled: ', cvx.trace(A2_labelled).value)

  # check correctness by looking at intersection of tangent cones for A1_labelled and A2_labelled
  # correct if and only if

  #  Tc(A1_labelled) ∩ - Tc(A2_labelled) ={0}

  if problem.status=='optimal':
    return problem.status,problem.value,A1_labelled.value,A2_labelled.value
  else:
    return problem.status,np.nan,np.nan,np.nan


if __name__ == '__main__':
  # A= K_4
  n = 4
  A=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3),)

  # A1 = cycle 
  A1=((0,1),(1,2),(2,3),(3,0),)

  # A2 = cross joining all nodes
  A2=((0,2),(1,3),)

  status,problem_value,A1_star,A2_star= deconvolve(n,A,A1,A2)

  A_matrix = create_adjacency_matrix(n,A)

  print('Problem status: ',status)
  print('Norm value: ',problem_value)
  print('A:  \n', A_matrix)
  print('A1: \n', np.round(A1_star,5))
  print('A2: \n', np.round(A2_star,5))
  print('A1+A2: \n ', np.round(np.add(A1_star,A2_star),5))

