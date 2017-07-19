from constraints.constraint import Constraint
import cvxpy as cvx
import numpy as np

class SchurHornOrbitopeConstraint(Constraint):

  def __init__(self, fixed_adjacency_matrix, variable_adjacency_matrix):
    super().__init__()
    self.orbitope(fixed_adjacency_matrix, variable_adjacency_matrix)

  def k_largest_eigenvalues(self, A,k):
    '''
    return array of length k of k largest eigenvalues of A, includes multiples
    '''
    eig_values = np.linalg.eigvalsh(A)[::-1] #sorted high to low,
    return eig_values[0:k]

  def construct_convex_hull(self,fixed_adjacency_matrix, variable_adjacency_matrix):
    constraints=[]

    m,n = fixed_adjacency_matrix.shape
    for i in range(1,n):
      constraints += [cvx.lambda_sum_largest(variable_adjacency_matrix,i) <= np.sum(self.k_largest_eigenvalues(fixed_adjacency_matrix,i))]
    
    constraints += [cvx.trace(variable_adjacency_matrix) == np.trace(fixed_adjacency_matrix)]
    self.constraint_list = constraints

