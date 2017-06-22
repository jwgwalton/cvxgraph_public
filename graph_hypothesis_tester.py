#!/usr/bin/env python3
import cvxpy as cvx
import numpy as np
from graphs.graph import Graph
from constraints.spectral_hull_constraint import SpectralHullConstraint
from constraints.diagonal_constraint import DiagonalConstraint
from constraints.degree_constraint import DegreeConstraint
from constraints.max_weighted_degree_constraint import MaxWeightedDegreeConstraint
from constraints.node_limit_constraint import NodeLimitConstraint

def test_family(A, M, constraints):

  objective = cvx.Maximize(cvx.trace(A*M))

  problem = cvx.Problem(objective,constraints)
  problem.solve()

  if problem.status=='optimal':
    return problem.value
  else:
    return np.nan


def generate_cycle_family_constraints(n,M):
  #cycle on 16 nodes
  A = ((0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10),(10,11),(11,12),(12,13),(13,14),(14,15),(15,0),)
  A_matrix = Graph.create_adjacency_matrix(n,A)

  # all values between 0 and 1
  limit_constraints = NodeLimitConstraint(M,0,1)

  # diag(A) == 0
  diagonal_constraints = DiagonalConstraint(n,M,0)    

  # all nodes have degree 2
  degree_constraints = DegreeConstraint(n,M,2)

  # TODO weird convex graph invariant

  # convex hull of 16 node cycles
  spectral_hull_constraint = SpectralHullConstraint(A_matrix,M)

  return limit_constraints.constraint_list + diagonal_constraints.constraint_list + degree_constraints.constraint_list + spectral_hull_constraint.constraint_list



def generate_sparse_well_connected_constraints(n,M):
  # sparse well-connected graphs on 16 nodes

  # all values between 0 and 1
  limit_constraints = NodeLimitConstraint(M,0,1)

  # diag(M) == 0
  diagonal_constraints = DiagonalConstraint(n,M,0)  

  # (A*ones)_i <= 2.5  
  degree_constraints = MaxWeightedDegreeConstraint(n,M,2.5)

  # TODO 2nd smalled eigenvalue of the laplacian must be >= 1.1


  return limit_constraints.constraint_list + diagonal_constraints.constraint_list + degree_constraints.constraint_list

  

if __name__ == '__main__':
  # a 16 node path (cycle with vertex removed
  n =16
  A = ((0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10),(10,11),(11,12),(12,13),(13,14),(14,15))
  A_matrix = Graph.create_adjacency_matrix(n,A)

  M = cvx.Symmetric(n)

  family_1_constraints = generate_cycle_family_constraints(n,M)
  family_2_constraints = generate_sparse_well_connected_constraints(n,M)

  family_1_similarity = test_family(A_matrix, M, family_1_constraints)
  family_2_similarity = test_family(A_matrix, M, family_2_constraints)

  print('First family similarity: ',family_1_similarity)
  print('Second family similarity: ',family_2_similarity)

  if family_1_similarity >= family_2_similarity:
    print('The first family is the best match for the graph')
  else:
    print('The second family is the best match for the graph')
