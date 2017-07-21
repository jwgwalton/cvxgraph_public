import numpy as np

class Graph(object):
  '''
  Generic graph class, allows access to graph object as adjacency list or adjacency matrix
  '''

  def __init__(self,n, adjacency_matrix=None, adjacency_list=None):
    self.number_of_nodes = n
    if adjacency_matrix is None and adjacency_list is None:
      raise ValueError('Pass in adjacency list or adjacency matrix to instantiate Graph object')
    if adjacency_matrix is None:
      self.adjacency_list = adjacency_list
      self.adjacency_matrix = self.create_adjacency_matrix(n, adjacency_list)
    if adjacency_list is None:
      self.adjacency_list = self.create_adjacency_list(n, adjacency_matrix)
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
    return tuple((i,j) for i in range(n) for j in range(i+1,n) if matrix[i,j])


if __name__ == '__main__': 
  # A= K_4
  n = 4
  A=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3),)

  A_matrix = Graph.create_adjacency_matrix(n,A)
  print(A_matrix)

  A_list = Graph.create_adjacency_list(n,A_matrix)
  print('Original edge list: ', A)
  print('Calculated edge list: ',A_list)



 
