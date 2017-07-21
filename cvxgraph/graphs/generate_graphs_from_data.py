#!/usr/bin/env python3
from graph_loader import GraphLoader
from permutation_matrix import PermutationMatrix
from graph import Graph

number_of_vertices=16
# clebsch graph
clebsch_file_path = 'data/clebsch.txt'
graph_loader_clebsch = GraphLoader(number_of_vertices, clebsch_file_path)
clebsch_graph =graph_loader_clebsch.load()
clebsch_matrix = clebsch_graph.adjacency_matrix

#shrikande graph
shrikhande_file_path = 'data/shrikhande.txt'
graph_loader_shrikhande = GraphLoader(number_of_vertices, shrikhande_file_path)
shrikhande_graph =graph_loader_shrikhande.load()
shrikhande_matrix = shrikhande_graph.adjacency_matrix

def contains_same_edge(A,B, tol):
  m,n = A.shape
  for i in range(0,n):
    for j in range(0,i):
      if A[i,j]>1-tol and B[i,j] > 1-tol: # if both matrices  == 1 at same 
        return True
  return False

while contains_same_edge(clebsch_matrix, shrikhande_matrix,0.1) is True:
  clebsch_matrix = PermutationMatrix.permute_matrix(clebsch_matrix)


# could test the adjacency lists
print('Clebsch Graph: ',Graph.create_adjacency_list(number_of_vertices,clebsch_matrix))
print('Shrikhande Graph: ',Graph.create_adjacency_list(number_of_vertices,shrikhande_matrix))
  

# Results from this, allows us to deconvolve

# Clebsch Graph:  ((0, 7), (0, 8), (0, 9), (0, 10), (0, 13), (1, 4), (1, 10), (1, 11), (1, 12), (1, 13), (2, 4), (2, 7), (2, 13), (2, 14), (2, 15), (3, 4), (3, 5), (3, 6), (3, 7), (3, 10), (4, 8), (4, 9), (5, 9), (5, 12), (5, 13), (5, 15), (6, 8), (6, 11), (6, 13), (6, 14), (7, 11), (7, 12), (8, 12), (8, 15), (9, 11), (9, 14), (10, 14), (10, 15), (11, 15), (12, 14))

# Shrikhande Graph:  ((0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 2), (1, 3), (1, 7), (1, 8), (1, 9), (2, 3), (2, 10), (2, 11), (2, 12), (3, 13), (3, 14), (3, 15), (4, 5), (4, 6), (4, 7), (4, 10), (4, 13), (5, 6), (5, 8), (5, 11), (5, 14), (6, 9), (6, 12), (6, 15), (7, 8), (7, 9), (7, 10), (7, 13), (8, 9), (8, 11), (8, 14), (9, 12), (9, 15), (10, 11), (10, 12), (10, 13), (11, 12), (11, 14), (12, 15), (13, 14), (13, 15), (14, 15))

