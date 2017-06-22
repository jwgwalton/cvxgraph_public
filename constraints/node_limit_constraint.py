from constraints.constraint import Constraint
import numpy as np
import cvxpy as cvx

class NodeLimitConstraint(Constraint):

  def __init__(self, adjacency_matrix,lower_limit, upper_limit):
    super().__init__()
    self.constraint_list=[adjacency_matrix>=lower_limit, adjacency_matrix<=upper_limit]
