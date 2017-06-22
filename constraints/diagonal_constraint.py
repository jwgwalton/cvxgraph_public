from constraints.constraint import Constraint

class DiagonalConstraint(Constraint):

  def __init__(self, n , matrix, constraint_value): 
    self.constraint_list=[matrix[i,i]==constraint_value for i in range(n)] # could calculate n from shape of matrix rather than pass in?
  
