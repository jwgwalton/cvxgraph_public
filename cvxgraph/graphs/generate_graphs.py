#!/usr/bin/env python3
from graph import Graph
from permutation_matrix import PermutationMatrix
n=16
# clebsch graph
A1=((0,1),(0,4),(0,7),(0,9),(0,10),(1,2),(1,5),(1,8),(1,11),(2,3),(2,6),(2,9),(2,12),(3,4),(3,5),(3,7),(3,13),(4,6),(4,8),(4,14),(5,10),(5,14),(5,15),(6,10),(6,11),(6,15),(7,11),(7,12),(7,15),(8,12),(8,13),(8,15),(9,13),(9,14),(9,15),(10,12),(10,13),(11,13),(11,14),(12,14),)

# shrikande graph
A2=((0,1),(0,2),(0,6),(0,7),(0,9),(0,15),(1,2),(1,3),(1,7),(1,8),(1,10),(2,3),(2,4),(2,9),(2,11),(3,4),(3,5),(3,10),(3,12),(4,5),(4,6),(4,11),(4,13),(5,6),(5,7),(5,12),(5,14),(6,7),(6,13),(6,15),(7,8),(7,14),(8,10),(8,11),(8,13),(8,14),(9,11),(9,12),(9,14),(9,15),(10,12),(10,13),(10,15),(11,13),(11,14),(12,14),(12,15),(13,15),)


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
print(Graph.create_adjacency_list(n,clebsch_matrix))
print(Graph.create_adjacency_list(n,shrikande_matrix))
  
