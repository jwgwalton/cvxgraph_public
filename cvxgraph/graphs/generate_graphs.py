#!/usr/bin/env python3
from graph import Graph
from graph_loader import GraphLoader
from permutation_matrix import PermutationMatrix

n=45
# 45 cycle  
A1=((0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10),(10,11),(11,12),(12,13),(13,14),(14,15),(15,16),(16,17),(17,18),(18,19),(19,20),(20,21),(21,22),(22,23),(23,24),(24,25),(25,26),(26,27),(27,28),(28,29),(29,30),(30,31),(31,32),(32,33),(33,34),(34,35),(35,36),(36,37),(37,38),(38,39),(39,40),(40,41),(41,42),(42,43),(43,44),(44,0),)

file_path = 'data/45_12_3_3.txt'
graph_loader = GraphLoader(n,file_path)
regular_graph = graph_loader.load()

cycle_matrix = Graph.create_adjacency_matrix(n,A1)
regular_graph_matrix = regular_graph.adjacency_matrix

def contains_same_edge(A,B, tol):
  m,n = A.shape # does this only work on numpy matrices?
  for i in range(0,n):
    for j in range(0,i):
      if A[i,j]>1-tol and B[i,j] > 1-tol: # if both matrices  == 1 at same 
        return True
  return False

while contains_same_edge(cycle_matrix, regular_graph_matrix, 0.1):
  cycle_matrix = PermutationMatrix.permute_matrix(cycle_matrix)

# could test the adjacency lists different
print('45 cycle: ',Graph.create_adjacency_list(n,cycle_matrix))
  
