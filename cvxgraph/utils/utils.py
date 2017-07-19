class Utils():

  @staticmethod
  def deep_equals(A,B, tol):
    '''
    check equality of symmetric matrices
    Args:
     A (matrix) 
     B (matrix)

    Returns
     bool, true if A_ij == B_ij
    '''
    m,n = A.shape # does this only work on numpy matrices?
    for i in range(0,n):
      for j in range(0,i):
        if abs(A[i,j]- B[i,j])>tol:
          return False
    return True

