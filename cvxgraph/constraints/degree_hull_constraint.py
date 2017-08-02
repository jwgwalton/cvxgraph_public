from constraints.constraint import Constraint
import cvxpy as cvx
import numpy as np

class DegreeHullConstraint(Constraint):

  def __init__(self, fixed_adjacency_matrix, variable_adjacency_matrix):
    super().__init__()
    self.construct_convex_hull(fixed_adjacency_matrix, variable_adjacency_matrix)

  def degree_sequence(self, n, matrix):
    # for the variable matrix i'm trying to take the cumulative sum of a matrix that doesn't exist
    degree_sequence= []
    print(matrix)
    for i in range(1,n):
      print(i)
      degree_sequence += [cvx.cumsum(matrix,i)]
    return np.sort(degree_sequence) #sorted is important

  def construct_convex_hull(self,fixed_adjacency_matrix, variable_adjacency_matrix):
    m,n = fixed_adjacency_matrix.shape
    constraints = [self.degree_sequence(n,variable_adjacency_matrix) == self.degree_sequence(n, fixed_adjacency_matrix)] 
    
    constraints += [cvx.trace(variable_adjacency_matrix) == np.trace(fixed_adjacency_matrix)]
    self.constraint_list = constraints


