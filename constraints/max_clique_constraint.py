from constraints.constraint import Constraint
import numpy as np

class MaxCliqueConstraint(Constraint):

  def __init__(self, A, max_clique_size): 
    self.constraint_list=[cvx.trace(A**max_clique_size)==0]

