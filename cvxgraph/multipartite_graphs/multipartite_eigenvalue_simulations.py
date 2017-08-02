#!/usr/bin/env python3
from generate_multipartite_graphs import complete_multipartite
from scipy.linalg import eigvalsh
import numpy as np

def run_simulation(min_vertices=1,max_vertices=5):
  file_path = 'results/complete_multipartite_eigenvalue_distribution.txt'
  f=open(file_path,'w')
  for i in range(min_vertices,max_vertices):
    for j in range(min_vertices,max_vertices):
      for k in range(min_vertices,max_vertices):
        eigenvalues = eigvalsh(complete_multipartite(p=(i,j,k,)))
        significant_figures = 10
        number_of_unique_eigenvalues = len(np.unique(np.round(eigenvalues,significant_figures)))
        f.write(str(i)+str(j)+str(k) + ' ' + str(number_of_unique_eigenvalues) +'\n')
  f.close()


if __name__ == '__main__':
  run_simulation(min_vertices=5,max_vertices=20)
