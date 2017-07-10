from constraints.constraint import Constraint
from constraints.max_clique_constraint import MaxCliqueConstraint
import cvxpy as cvx

class TriangleFreeConstraint(Constraint):

  def __init__(self, A): 
    B= cvx.power(A,3)
    self.constraint_list=[cvx.trace(B)==0]
