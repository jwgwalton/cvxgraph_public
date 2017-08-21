#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', ))
from graphs.graph import Graph
import numpy as np

def cycle(n):
  A=np.zeros((n,n))
  for i in range(n-1): A[i,i+1]=A[i+1,i]=1
  A[0,n-1]=A[n-1,0]=1
  return A

def bicycle(n):
  A=cycle(n)
  A[0,n//2]=A[n//2,0]=1
  return A

# 8 node bicycle
n=8
A=bicycle(n)
eig_values = np.linalg.eigvalsh(A)
print('8 node bicycle eigenvalues: ',eig_values)


# 16 node bicycle
n=16
A=bicycle(n)
eig_values = np.linalg.eigvalsh(A)
print('16 node bicycle eigenvalues: ',eig_values)
