#!/usr/bin/env python3
import numpy as np
from graphs.graph import Graph

class GraphLoader():

  def __init__(self, n, file_path):
    self.n = n
    self.file_path = file_path

  def load(self):
    adjacency_matrix = np.loadtxt(self.file_path, dtype=int)
    print(adjacency_matrix)
    return Graph(self.n,adjacency_matrix=adjacency_matrix)

if __name__ == '__main__':
  # will cry about graphs.graph import, need to sort out relative imports from project root
  n=9
  file_path = 'data/9_4_1_2.txt'
  graph_loader = GraphLoader(n,file_path)
  graph = graph_loader.load()

  print(graph.adjacency_matrix)
  print(graph.adjacency_list)
