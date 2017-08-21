from constraints.constraint import Constraint
import cvxpy as cvx
import numpy as np

class SpectralHullConstraint(Constraint):

  def __init__(self, fixed_adjacency_matrix, variable_adjacency_matrix,epsilon_vector):
    super().__init__()
    self.epsilon_vector = epsilon_vector
    self.eigenvalues = np.linalg.eigvalsh(fixed_adjacency_matrix)[::-1] # viewed high to low
    self.construct_convex_hull(fixed_adjacency_matrix, variable_adjacency_matrix)


  def k_largest_eigenvalues(self,k):
    '''
    return array of length k of k largest eigenvalues of A, includes multiples
    '''
    return self.eigenvalues[:k]

  def construct_convex_hull(self,fixed_adjacency_matrix, variable_adjacency_matrix):
    n = fixed_adjacency_matrix.shape[0]

    constraints = [cvx.lambda_sum_largest(variable_adjacency_matrix,i+1) <= np.sum(self.k_largest_eigenvalues(i+1)) + self.epsilon_vector[i] for i in range(n)]
    
    constraints += [cvx.trace(variable_adjacency_matrix) == np.trace(fixed_adjacency_matrix)]

    self.constraint_list = constraints


