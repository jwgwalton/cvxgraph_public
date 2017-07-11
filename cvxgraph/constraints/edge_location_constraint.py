from constraints.constraint import Constraint

class EdgeLocationConstraint(Constraint):

  def __init__(self, n , fixed_matrix, variable_matrix, constraint_value): 
    super().__init__()
    for i in range(0,n):
      for j in range(0,i):
        if fixed_matrix[i,j] == constraint_value and i != j: 
          self.constraint_list += [variable_matrix[i,j] == constraint_value] 

  
