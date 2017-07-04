#!/usr/bin/env python3
import cvxpy as cvx
import numpy as np
from constraints.spectral_hull_constraint import SpectralHullConstraint
from constraints.node_limit_constraint import NodeLimitConstraint
from graphs.graph import Graph

def deconvolve(n,A,A1,A2):
  '''
  n: number of nodes/dimension of adjacency matrix
  A: Composition of A1 and A2, don't know labelling
  A1: Component of A
  A2: component of A
  '''
  A_matrix  = Graph.create_adjacency_matrix(n,A)
  A1_matrix = Graph.create_adjacency_matrix(n,A1)
  A2_matrix = Graph.create_adjacency_matrix(n,A2)

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

  # check correctness by looking at intersection of tangent cones for A1_labelled and A2_labelled
  # correct if and only if

  #  Tc(A1_labelled) ∩ - Tc(A2_labelled) ={0}

  if problem.status=='optimal':
    return problem.status,problem.value,A1_labelled.value,A2_labelled.value
  else:
    return problem.status,np.nan,np.nan,np.nan


if __name__ == '__main__':
  n=16
  #  check size(A) = size(A1)+ size(A2)
  A = ((0,1),(0,4),(0,7),(0,9),(0,10),(1,2),(1,5),(1,8),(1,11),(2,3),(2,6),(2,9),(2,12),(3,4),(3,5),(3,7),(3,13),(4,6),(4,8),(4,14),(5,10),(5,14),(5,15),(6,10),(6,11),(6,15),(7,11),(7,12),(7,15),(8,12),(8,13),(8,15),(9,13),(9,14),(9,15),(10,12),(10,13),(11,13),(11,14),(12,14),(0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)
  
  #16 cycle
  A1 = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)

  #clebsch graph
  A2=((0,1),(0,4),(0,7),(0,9),(0,10),(1,2),(1,5),(1,8),(1,11),(2,3),(2,6),(2,9),(2,12),(3,4),(3,5),(3,7),(3,13),(4,6),(4,8),(4,14),(5,10),(5,14),(5,15),(6,10),(6,11),(6,15),(7,11),(7,12),(7,15),(8,12),(8,13),(8,15),(9,13),(9,14),(9,15),(10,12),(10,13),(11,13),(11,14),(12,14),)

  status,problem_value,A1_star,A2_star= deconvolve(n,A,A1,A2)
  A_matrix = Graph.create_adjacency_matrix(n,A)
  np.set_printoptions(suppress=True)
  print('Problem status: ',status)
  print('Norm value: ',problem_value)
  print('A:  \n', A_matrix)
  print('A1: \n', A1_star)
  print('A2: \n', A2_star)
  print('A1+A2: \n ', np.add(A1_star,A2_star))

