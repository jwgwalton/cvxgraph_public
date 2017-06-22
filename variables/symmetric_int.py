import cvxpy as cvx

def SymmetricInt(n):
  '''
  Returns a n*n symmetric integer matrix
  current method in cvxpy to force a variable to have multiple properties
  '''
  symmetric = cvx.Symmetric(n)
  integer = cvx.Int(n,n)
  return (symmetric = integer)
