from constraints.constraint import Constraint
import numpy as np

class DegreeConstraint(Constraint):

  def __init__(self, n , A, max_degree): 
    self.constraint_list=self.create_constraints(n,A,max_degree)

  def create_constraints(self,n,A,max_degree):
    one_vec=np.ones(n)
    return [(1/max_degree)*A*one_vec == one_vec]
  
