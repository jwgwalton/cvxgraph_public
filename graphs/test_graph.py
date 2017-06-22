#!/usr/bin/env python3
from graph import *

# A= K_4
n = 4
A=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3),)


A_matrix = Graph.create_adjacency_matrix(n,A)
print(A_matrix)

A_list = Graph.create_adjacency_list(n,A_matrix)
print('Original edge list: ', A)
print('Calculated edge list: ',A_list)
