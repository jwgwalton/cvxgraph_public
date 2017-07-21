#!/usr/bin/env python3
from graph import Graph
from permutation_matrix import PermutationMatrix
n=16
# 16 cycle  
A1=((7,1),(1,6),(6,5),(5,0),(0,8),(8,3),(3,9),(9,14),(14,13),(13,12),(12,11),(11,10),(10,9),(9,7),(7,15),(15,7),)

# Shrikhande Graph: 
A2=((0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(1,2),(1,3),(1,7),(1,8),(1,9),(2,3),(2,10),(2,11),(2,12),(3,13),(3,14),(3,15),(4,5),(4,6),(4,7),(4,10),(4,13),(5,6),(5,8),(5,11),(5,14),(6,9),(6,12),(6,15),(7,8),(7,9),(7,10),(7,13),(8,9),(8,11),(8,14),(9,12),(9,15),(10,11),(10,12),(10,13),(11,12),(11,14),(12,15),(13,14),(13,15),(14,15),)


clebsch_matrix = Graph.create_adjacency_matrix(n,A1)
shrikande_matrix = Graph.create_adjacency_matrix(n,A2)

def contains_same_edge(A,B, tol):
  m,n = A.shape # does this only work on numpy matrices?
  for i in range(0,n):
    for j in range(0,i):
      if A[i,j]>1-tol and B[i,j] > 1-tol: # if both matrices  == 1 at same 
        return True
  return False

while contains_same_edge(clebsch_matrix, shrikande_matrix, 0.1):
  clebsch_matrix = PermutationMatrix.permute_matrix(clebsch_matrix)

# could test the adjacency lists different
print('16 cycle: ',Graph.create_adjacency_list(n,clebsch_matrix))
print('shrikhande graph: ',Graph.create_adjacency_list(n,shrikande_matrix))
  
