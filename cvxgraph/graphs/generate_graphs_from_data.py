#!/usr/bin/env python3
from graph_loader import GraphLoader
from permutation_matrix import PermutationMatrix
from graph import Graph

number_of_vertices=16
# clebsch graph
clebsch_file_path = 'graphs/data/clebsch.txt'
graph_loader_clebsch = GraphLoader(number_of_vertices, clebsch_file_path)
clebsch_graph =graph_loader_clebsch.load()
clebsch_matrix = clebsch_graph.adjacency_matrix

#shrikande graph
shrikhande_file_path = 'graphs/data/shrikhande.txt'
graph_loader_shrikhande = GraphLoader(number_of_vertices, shrikhande_file_path)
shrikhande_graph =graph_loader_shrikhande.load()
shrikande_matrix = shrikhande_graph.adjacency_matrix

def contains_same_edge(A,B, tol):
  m,n = A.shape
  for i in range(0,n):
    for j in range(0,i):
      if A[i,j]>1-tol and B[i,j] > 1-tol: # if both matrices  == 1 at same 
        return True
  return False

while contains_same_edge(clebsch_matrix, shrikande_matrix,0.1) is True:
  clebsch_matrix = PermutationMatrix.permute_matrix(clebsch_matrix)
  shrikande_matrix = PermutationMatrix.permute_matrix(shrikande_matrix)


# could test the adjacency lists
print('Clebsch Graph: ',Graph.create_adjacency_list(clebsch_matrix))
print('Shrikhande Graph: ',Graph.create_adjacency_list(shrikhande_matrix))
  
