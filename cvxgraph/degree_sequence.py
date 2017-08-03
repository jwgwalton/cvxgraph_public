#!/usr/bin/env python3
import numpy as np
from graphs.graph import Graph
from multipartite_graphs.generate_multipartite_graphs import complete_multipartite


def calculate_degree_sequence(partitions):
  degree_sequence = []
  for partition in partitions:
    degree=0
    other_partitions = list(partitions)
    other_partitions.remove(partition) #awful, must be way to search through list of other tuples, condition on != breaks if all partitions same size

    for other_partition in other_partitions:
        degree += other_partition
    degree_sequence.extend(degree*np.ones(partition))
  return np.sort(degree_sequence)

def check_degree_sequence(partitions, matrix):
  expected_degree_sequence = calculate_degree_sequence(partitions)
  actual_degree_sequence = np.sort(np.sum(matrix,axis=0))
  #print('expected_degree_sequence: ',expected_degree_sequence)
  #print('actual_degree_sequence: ',actual_degree_sequence)
  return np.allclose(expected_degree_sequence, actual_degree_sequence)

if __name__=='__main__':
  n=16
  # (8,8) graph
  p=(8,8)
  multipartite_graph_adj_matrix =complete_multipartite(p)

  print(check_degree_sequence(p,multipartite_graph_adj_matrix))
