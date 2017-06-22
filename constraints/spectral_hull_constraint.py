from constraints.constraint import Constraint
import numpy as np
import cvxpy as cvx

class SpectralHullConstraint(Constraint):

  def __init__(self, fixed_adjacency_matrix, variable_adjacency_matrix):
    super().__init__()
    self.construct_convex_hull(fixed_adjacency_matrix, variable_adjacency_matrix)

  def construct_convex_hull(self,fixed_adjacency_matrix, variable_adjacency_matrix):

    sum_of_eigen_values = sum(np.linalg.eigvalsh(fixed_adjacency_matrix))
    trace = cvx.trace(fixed_adjacency_matrix)

    m,n = fixed_adjacency_matrix.shape
    
    #should i be doing this by using add method?
    self.constraint_list = [cvx.trace(variable_adjacency_matrix) == trace, cvx.lambda_sum_largest(variable_adjacency_matrix,n) <= sum_of_eigen_values]
