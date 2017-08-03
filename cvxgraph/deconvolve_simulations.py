#!/usr/bin/env python3
import numpy as np
import random
from deconvolve import GraphDeconvolver
from graphs.graph import Graph

########################################################
# Test permuting the labellings of the convolved graph #
########################################################

def permute_matrix(A):
  m,n = np.shape(A)
  p = random.sample(range(0,n),n)
  A[:,:] = A[p,:] 
  A[:,:] = A[:,p]
  return A

# Graphs
n=16
#  check size(A) = size(A1)+ size(A2)
A = ((0,1),(0,4),(0,7),(0,9),(0,10),(1,2),(1,5),(1,8),(1,11),(2,3),(2,6),(2,9),(2,12),(3,4),(3,5),(3,7),(3,13),(4,6),(4,8),(4,14),(5,10),(5,14),(5,15),(6,10),(6,11),(6,15),(7,11),(7,12),(7,15),(8,12),(8,13),(8,15),(9,13),(9,14),(9,15),(10,12),(10,13),(11,13),(11,14),(12,14),(0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)
  
#16 cycle
A1 = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)

#clebsch graph
A2=((0,1),(0,4),(0,7),(0,9),(0,10),(1,2),(1,5),(1,8),(1,11),(2,3),(2,6),(2,9),(2,12),(3,4),(3,5),(3,7),(3,13),(4,6),(4,8),(4,14),(5,10),(5,14),(5,15),(6,10),(6,11),(6,15),(7,11),(7,12),(7,15),(8,12),(8,13),(8,15),(9,13),(9,14),(9,15),(10,12),(10,13),(11,13),(11,14),(12,14),)


A_matrix  = Graph.create_adjacency_matrix(n,A)

correct_count = 0
iterations = 100

graph_deconvolver = GraphDeconvolver(n,A1,A2)

for i in range(1,iterations):
  status,problem_value,A1_star,A2_star= graph_deconvolver.deconvolve(A_matrix)
  print('Problem status: ',status)
  cycle = is_cycle(Graph.create_adjacency_list(n,A1_star))
  print('Is cycle: ', cycle)
  if cycle:
   correct_count +=1

print(str(correct_count)+' correct out of '+str(iterations)+' iterations')
