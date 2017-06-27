from constraints.constraint import Constraint
import numpy as np
import cvxpy as cvx

class LaplacianLambdaSecondMinConstraint(Constraint):

  def __init__(self, A, lower_limit):
    super().__init__()
    self.constraint_list=[cvx.lambda_sum_smallest(self.laplacian(A),2)>=lower_limit]

  def laplacian(self, matrix):
    m,n = np.size(matrix)
    one_vec = np.ones(n)
    D = cvx.diag(matrix*one_vec)
    return D - matrix
