import cvxpy as cvx

def SymmetricInt(n):
  '''
  Returns a n*n symmetric integer matrix
  current method in cvxpy to force a variable to have multiple properties
  '''
  integer = cvx.Int(n,n)
  symmetric = cvx.Symmetric(n)
  symmetric = integer
  return symmetric
