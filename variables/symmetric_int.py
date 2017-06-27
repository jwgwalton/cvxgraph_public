import cvxpy as cvx

def SymmetricInt(n):
  '''
  Returns a n*n symmetric integer matrix
  current method in cvxpy to force a variable to have multiple properties
  '''
  integer_matrix = cvx.Int(n,n)
  symmetric_matrix = cvx.Symmetric(n)
  symmetric_matrix = integer_matrix
  return symmetric_matrix
