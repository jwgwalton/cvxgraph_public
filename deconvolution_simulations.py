#!/usr/bin/env python3
import numpy as np
from deconvolve import GraphDeconvolver
from graphs.graph import Graph

def generate_permutation_matrix(n):
  I = np.identity(n)
  p = np.random.randint(0,high=2,size=n) #permutation vector
  I[:,:] = I[p,:] 
  I[:,:] = I[:,p]
  return I

def permute_matrix(A):
  m,n = np.shape(A)
  permutation_matrix = generate_permutation_matrix(n)
  return permutation_matrix*A*permutation_matrix.T

# Graphs
# A= K_4
n = 4
A=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3),)

# A1 = cycle 
A1=((0,1),(1,2),(2,3),(3,0),)

# A2 = cross joining all nodes
A2=((0,2),(1,3),)


A_matrix  = Graph.create_adjacency_matrix(n,A)

correct_count = 0
iterations = 10

graph_deconvolver = GraphDeconvolver(n,A1,A2)

for i in range(1,iterations):
  status,is_correct,problem_value,A1_star,A2_star= graph_deconvolver.deconvolve(A_matrix)
  print('Problem correct: ', is_correct)
  if is_correct == True:
    correct_count +=1
  A_matrix= permute_matrix(A_matrix)


print(str(correct_count)+' correct out of '+str(iterations)+' iterations')
