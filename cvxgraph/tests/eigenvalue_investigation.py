#!/usr/bin/env python3
from graphs.graph import Graph
import numpy as np

# clebsch graph
n=16
A=((0,1),(0,4),(0,7),(0,9),(0,10),(1,2),(1,5),(1,8),(1,11),(2,3),(2,6),(2,9),(2,12),(3,4),(3,5),(3,7),(3,13),(4,6),(4,8),(4,14),(5,10),(5,14),(5,15),(6,10),(6,11),(6,15),(7,11),(7,12),(7,15),(8,12),(8,13),(8,15),(9,13),(9,14),(9,15),(10,12),(10,13),(11,13),(11,14),(12,14),)

A_matrix  = Graph.create_adjacency_matrix(n,A)
eig_values = np.linalg.eigvalsh(A_matrix)

print('Clebsch graph eigenvalues: ',eig_values)



# clebsch graph (missing(0,1))
n=16
A=((0,4),(0,7),(0,9),(0,10),(1,2),(1,5),(1,8),(1,11),(2,3),(2,6),(2,9),(2,12),(3,4),(3,5),(3,7),(3,13),(4,6),(4,8),(4,14),(5,10),(5,14),(5,15),(6,10),(6,11),(6,15),(7,11),(7,12),(7,15),(8,12),(8,13),(8,15),(9,13),(9,14),(9,15),(10,12),(10,13),(11,13),(11,14),(12,14),)

A_matrix  = Graph.create_adjacency_matrix(n,A)
eig_values = np.linalg.eigvalsh(A_matrix)

print('Clebsch graph with missing edge eigenvalues: ',eig_values)



# cycle
n=16
A = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)

A_matrix  = Graph.create_adjacency_matrix(n,A)
eig_values = np.linalg.eigvalsh(A_matrix)

print('Cycle graph eigenvalues: ',eig_values)


# cycle: missing edge (0,5)
n=16
A = ((5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)

A_matrix  = Graph.create_adjacency_matrix(n,A)
eig_values = np.linalg.eigvalsh(A_matrix)

print('Cycle graph with missing edge eigenvalues: ',eig_values)


# shrikande graph
n=16
A=((0,1),(0,2),(0,6),(0,7),(0,9),(0,15),(1,2),(1,3),(1,7),(1,8),(1,10),(2,3),(2,4),(2,9),(2,11),(3,4),(3,5),(3,10),(3,12),(4,5),(4,6),(4,11),(4,13),(5,6),(5,7),(5,12),(5,14),(6,7),(6,13),(6,15),(7,8),(7,14),(8,10),(8,11),(8,13),(8,14),(9,11),(9,12),(9,14),(9,15),(10,12),(10,13),(10,15),(11,13),(11,14),(12,14),(12,15),(13,15),)

A_matrix  = Graph.create_adjacency_matrix(n,A)
eig_values = np.linalg.eigvalsh(A_matrix)

print('Shrikande graph eigenvalues: ',eig_values)

# shrikande graph missing (13,15)
n=16
A=((0,1),(0,2),(0,6),(0,7),(0,9),(0,15),(1,2),(1,3),(1,7),(1,8),(1,10),(2,3),(2,4),(2,9),(2,11),(3,4),(3,5),(3,10),(3,12),(4,5),(4,6),(4,11),(4,13),(5,6),(5,7),(5,12),(5,14),(6,7),(6,13),(6,15),(7,8),(7,14),(8,10),(8,11),(8,13),(8,14),(9,11),(9,12),(9,14),(9,15),(10,12),(10,13),(10,15),(11,13),(11,14),(12,14),(12,15),)

A_matrix  = Graph.create_adjacency_matrix(n,A)
eig_values = np.linalg.eigvalsh(A_matrix)

print('Shrikande graph with missing edge eigenvalues: ',eig_values)
