from constraints.max_clique_constraint import MaxCliqueConstraint
import cvxpy as cvx

class TriangleFreeConstraint(MaxCliqueConstraint):

  def __init__(self, A): 
    self.constraint_list=[cvx.trace(cvx.power(A,3))==0]
