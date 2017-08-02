#!/usr/bin/env python3
from graph_loader import GraphLoader
from permutation_matrix import PermutationMatrix
from graph import Graph

number_of_vertices=16
# clebsch graph
clebsch_list = ((0,7),(0,8),(0,9),(0,10),(0,13),(1,4),(1,10),(1,11),(1,12),(1,13),(2,4),(2,7),(2,13),(2,14),(2,15),(3,4),(3,5),(3,6),(3,7),(3,10),(4,8),(4,9),(5,9),(5,12),(5,13),(5,15),(6,8),(6,11),(6,13),(6,14),(7,11),(7,12),(8,12),(8,15),(9,11),(9,14),(10,14),(10,15),(11,15),(12,14))
clebsch_matrix = Graph.create_adjacency_matrix(number_of_vertices,clebsch_list)

#shrikande graph
shrikhande_list = ((0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(1,2),(1,3),(1,7),(1,8),(1,9),(2,3),(2,10),(2,11),(2,12),(3,13),(3,14),(3,15),(4,5),(4,6),(4,7),(4,10),(4,13),(5,6),(5,8),(5,11),(5,14),(6,9),(6,12),(6,15),(7,8),(7,9),(7,10),(7,13),(8,9),(8,11),(8,14),(9,12),(9,15),(10,11),(10,12),(10,13),(11,12),(11,14),(12,15),(13,14),(13,15),(14,15))
shrikhande_matrix = Graph.create_adjacency_matrix(number_of_vertices,shrikhande_list)

#convolved shrikhande and clebsch
convolved_matrix = clebsch_matrix+shrikhande_matrix

# 16 node cycle
cycle = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)
cycle_matrix = Graph.create_adjacency_matrix(number_of_vertices,cycle)

def contains_same_edge(A,B,tol):
  m,n = A.shape
  for i in range(0,n):
    for j in range(0,i):
      if A[i,j]>1-tol and B[i,j] > 1-tol: # if both matrices  == 1 at same 
        return True
  return False

while contains_same_edge(cycle_matrix,convolved_matrix,0.1) is True:
  cycle_matrix = PermutationMatrix.permute_matrix(cycle_matrix)


# distinct cycle for multi deconvolve
print('Cycle matrix: ',Graph.create_adjacency_list(number_of_vertices,cycle_matrix))
  

# Results from this,allows us to have 3 distinct graphs

# Clebsch Graph:  ((0,7),(0,8),(0,9),(0,10),(0,13),(1,4),(1,10),(1,11),(1,12),(1,13),(2,4),(2,7),(2,13),(2,14),(2,15),(3,4),(3,5),(3,6),(3,7),(3,10),(4,8),(4,9),(5,9),(5,12),(5,13),(5,15),(6,8),(6,11),(6,13),(6,14),(7,11),(7,12),(8,12),(8,15),(9,11),(9,14),(10,14),(10,15),(11,15),(12,14))

# Shrikhande Graph:  ((0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(1,2),(1,3),(1,7),(1,8),(1,9),(2,3),(2,10),(2,11),(2,12),(3,13),(3,14),(3,15),(4,5),(4,6),(4,7),(4,10),(4,13),(5,6),(5,8),(5,11),(5,14),(6,9),(6,12),(6,15),(7,8),(7,9),(7,10),(7,13),(8,9),(8,11),(8,14),(9,12),(9,15),(10,11),(10,12),(10,13),(11,12),(11,14),(12,15),(13,14),(13,15),(14,15))

# Cycle Graph:  ((0, 12), (0, 15), (1, 14), (1, 15), (2, 6), (2, 8), (3, 8), (3, 11), (4, 11), (4, 14), (5, 7), (5, 10), (6, 7), (9, 10), (9, 13), (12, 13))

