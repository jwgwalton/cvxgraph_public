#!/usr/bin/env python3
import numpy as np

class Graph(object):
  '''
  Generic graph class, allows access to graph object as adjacency list or adjacency matrix
  '''

  def __init__(self,n, adjacency_matrix=None, adjacency_list=None):
    self.number_of_nodes = n
    # expects one or other to be populated, is this most pythonic way?
    if adjacency_matrix == None:
      self.adjacency_list = adjacency_list
      self.adjacency_matrix = create_adjacency_matrix(n, adjacency_list)
    if adjacency_list == None:
      self.adjacency_list = create_adjacency_list(n, adjacency_matrix)
      self.adjacency_matrix = adjacency_matrix
  
  @staticmethod
  def create_adjacency_matrix(n, edge_list):
    adjacency_matrix = np.zeros((n,n))
    for i,j in edge_list:
      adjacency_matrix[i][j]=1
      adjacency_matrix[j][i]=1
    return adjacency_matrix

  @staticmethod
  def create_adjacency_list(n, matrix):
    '''
    create an adjacency list from an adjaceny matrix
    '''
    edge_list=[]
    for j in range(n):
      for i in range(j):
        if matrix[i,j] > 0: 
          edge_list.append((i,j))
    return tuple(edge_list)

if __name__ == '__main__': 
  # A= K_4
  n = 4
  A=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3),)

  A_matrix = Graph.create_adjacency_matrix(n,A)
  print(A_matrix)

  A_list = Graph.create_adjacency_list(n,A_matrix)
  print('Original edge list: ', A)
  print('Calculated edge list: ',A_list)



 
