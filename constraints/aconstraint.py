from constraints.constraint import Constraint
import numpy as np
import cvxpy as cvx

class AConstraint(Constraint):

  def __init__(self, adjacency_matrix):
    super().__init__()
    self.add_constraint([adjacency_matrix>=0, adjacency_matrix<=1] )
