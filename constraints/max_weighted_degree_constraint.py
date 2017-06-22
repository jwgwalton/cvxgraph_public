from constraints.constraint import Constraint
import numpy as np

class MaxWeightedDegreeConstraint(Constraint):

  def __init__(self, n , A, max_weighted_degree): 
    self.constraint_list=self.create_constraints(n,A,max_weighted_degree)

  def create_constraints(self,n,A,max_weighted_degree):
    one_vec=np.ones(n)
    return [A*one_vec == max_weighted_degree]
  
