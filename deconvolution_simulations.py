#!/usr/bin/env python3
import numpy as np
from deconvolve import deconvolve
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
n=16
# convolved graphs
A = ((0,1),(0,4),(0,7),(0,9),(0,10),(1,2),(1,5),(1,8),(1,11),(2,3),(2,6),(2,9),(2,12),(3,4),(3,5),(3,7),(3,13),(4,6),(4,8),(4,14),(5,10),(5,14),(5,15),(6,10),(6,11),(6,15),(7,11),(7,12),(7,15),(8,12),(8,13),(8,15),(9,13),(9,14),(9,15),(10,12),(10,13),(11,13),(11,14),(12,14),(0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)
  
#16 cycle
A1 = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)

#clebsch graph
A2=((0,1),(0,4),(0,7),(0,9),(0,10),(1,2),(1,5),(1,8),(1,11),(2,3),(2,6),(2,9),(2,12),(3,4),(3,5),(3,7),(3,13),(4,6),(4,8),(4,14),(5,10),(5,14),(5,15),(6,10),(6,11),(6,15),(7,11),(7,12),(7,15),(8,12),(8,13),(8,15),(9,13),(9,14),(9,15),(10,12),(10,13),(11,13),(11,14),(12,14),)

A_matrix  = Graph.create_adjacency_matrix(n,A)
A1_matrix = Graph.create_adjacency_matrix(n,A1)
A2_matrix = Graph.create_adjacency_matrix(n,A2)

correct_count = 0
iterations = 10

for i in range(1,iterations):
  status,is_correct,problem_value,A1_star,A2_star= deconvolve(n,A_matrix,A1_matrix,A2_matrix)
  print('Problem correct: ', is_correct)
  if is_correct == True:
    correct_count +=1
  A_matrix= permute_matrix(A_matrix)


print(str(correct_count)+' correct out of '+str(iterations)+' iterations')
