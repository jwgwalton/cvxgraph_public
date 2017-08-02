#!/usr/bin/env python3
# Keith Briggs 2017-08-02

from math import cos,pi
import numpy as np
from itertools import combinations
from scipy.linalg import eigvalsh

np.set_printoptions(linewidth=200,suppress=True)

def complete_multipartite(p=(3,3,3,)):
  n=sum(p)
  A=np.zeros((n,n))
  i,spans=0,[]
  for pi in p:
    spans.append((i,i+pi))
    i+=pi
  print('spans=',spans)
  for c0,c1 in combinations(spans,2):
    for i in range(*c0):
      for j in range(*c1):
        A[i,j]=A[j,i]=1
  return A

if __name__=='__main__':
  A=complete_multipartite()
  print(A)
  ev=eigvalsh(A)
  print(ev)
