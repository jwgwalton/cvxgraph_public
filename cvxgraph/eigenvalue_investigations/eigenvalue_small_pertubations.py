#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', ))
from graphs.graph import Graph
from graphs.graph_loader import GraphLoader
import numpy as np

def perturb_matrix(n,matrix):
  pertubation_matrix = np.random.normal(scale=0.0001,size=(n,n))
  return matrix+pertubation_matrix

def run_simulation(n, graph_name):
  number_of_simulations=100000
  file_path = '../graphs/data/'+graph_name+'.txt'
  graph_loader = GraphLoader(n,file_path)
  graph = graph_loader.load()

  A_matrix = graph.adjacency_matrix
  eigenvalues_A = np.linalg.eigvalsh(A_matrix)

  file_path = 'results/'+graph_name+'_eigenvalues_small_pertubation.txt'
  f=open(file_path,'w')
  fmt='%.3f '*n
  for i in range(number_of_simulations):
    A_permuted = perturb_matrix(n,A_matrix.copy())
    difference = np.linalg.eigvalsh(A_permuted) - eigenvalues_A
    norm = np.linalg.norm(difference)
    #f.write(fmt%tuple(difference)+'\n')
    f.write('%.6f\n'%(norm,))
  f.close()

if __name__ == '__main__':
  run_simulation(16, 'clebsch')
  run_simulation(16, 'shrikhande')
  run_simulation(17, '17_8_3_4')
  run_simulation(64, '64_18_2_6')
  run_simulation(9, '9_4_1_2')
