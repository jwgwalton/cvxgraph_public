import numpy as np





class Graph(object):
  '''
  Generic graph class, allows access to graph object as adjacency list or adjacency matrix
  '''

  def __init__(self,n, graph):
    # check type of input, if tuple set it as adjacency list and generate adjacency matrix, vice versa
    # most pythonic way of doing this?
    self.number_of_nodes = n
    self.adjacency_list = graph
    self.adjacency_matrix = create_adjacency_matrix(self, n, graph)
  
  @staticmethod
  def create_adjacency_matrix(n, edge_list):
    adjacency_matrix = np.zeros((n,n))
    for k in range(len(edge_list)):
      i,j = edge_list[k]
      adjacency_matrix[i][j]=1
      adjacency_matrix[j][i]=1
    return adjacency_matrix

  @staticmethod
  def create_adjacency_list(self, n, matrix):
    '''
    create an adjacency list from an adjaceny matrix
    '''
    pass



 
