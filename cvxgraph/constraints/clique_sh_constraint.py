from constraints.constraint import Constraint
import cvxpy as cvx
import numpy as np

class CliqueSchurHornOrbitopeConstraint(Constraint):

  def __init__(self, fixed_adjacency_matrix, variable_adjacency_matrix, clique_size):
    super().__init__()
    self.construct_orbitope(fixed_adjacency_matrix, variable_adjacency_matrix, clique_size)

  def construct_orbitope(self,fixed_adjacency_matrix, variable_adjacency_matrix,clique_size):
    m,n = fixed_adjacency_matrix.shape
    # equality constraint to make variable matrix be positive semi definite
    P = cvx.Semidef(n)

    self.constraint_list = [cvx.trace(variable_adjacency_matrix) == clique_size, variable_adjacency_matrix == P]

