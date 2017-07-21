import numpy as np
import random

class PermutationMatrix():

  @staticmethod
  def permute_matrix(A):
    m,n = np.shape(A)
    p = random.sample(range(0,n),n)
    A[:,:] = A[p,:] 
    A[:,:] = A[:,p]
    return A



