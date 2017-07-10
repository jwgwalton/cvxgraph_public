from constraints.constraint import Constraint
import cvxpy as cvx

class MaxCliqueConstraint(Constraint):

  def __init__(self, A, max_clique_size): 
    self.constraint_list=clique_constraint(A,max_clique_size)

  @staticmethod
  def clique_constraint(A,max_clique_size):
    return [cvx.trace(cvx.power(A,max_clique_size))==0]
