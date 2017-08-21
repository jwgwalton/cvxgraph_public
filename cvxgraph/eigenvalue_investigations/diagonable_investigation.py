#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', ))
from graphs.graph import Graph
from graphs.graph_loader import GraphLoader
import numpy as np
from sympy import Matrix, pprint


def load_graph(n,graph_name):
  file_path = '../graphs/data/'+graph_name+'.txt'
  graph_loader = GraphLoader(n,file_path)
  return graph_loader.load()

def run_simulation(n, graph_name):
  graph = load_graph(n,graph_name)
  A_matrix = graph.adjacency_matrix
  sympy_matrix = Matrix(A_matrix)

  P,J = sympy_matrix.jordan_form()

  #pprint(P)

  pprint(J)


if __name__ == '__main__':
  run_simulation(16, 'clebsch')
