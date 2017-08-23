#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', ))
import numpy as np
import random
from denoise import GraphDenoiser
from graphs.graph import Graph
from graphs.graph_visualiser import GraphVisualiser
from multipartite_graphs.generate_multipartite_graphs import complete_multipartite
from degree_sequence import check_degree_sequence
from multipartite_graphs.multipartite_graph_recognizer_02 import Multipartite_graph_recognizer
from gaussian_noise_perturb import perturb_matrix

#####################################################################################
# Test deconvolve complete multipartite graphs with small pertubations #
#####################################################################################

def run_simulation(n, multipartite_graph_matrix, iterations, partitions, perturbation_scale = 0.1):
  correct_count = 0

  graph_denoiser = GraphDenoiser(n,Graph.create_adjacency_list(n,multipartite_graph_matrix))
  

  # vector of small parameters for spectral hull
  epsilon_vector = epsilon*np.ones(n)

  for i in range(0,iterations):

    A_matrix_noisy = perturb_matrix(multipartite_graph_matrix, perturbation_scale)

    status,problem_value,A_recovered= graph_denoiser.denoise(A_matrix_noisy,epsilon_vector)

    # first check has the correct degree sequence before check multipartite, (needs to be complete)
    correct_degree_sequence = check_degree_sequence(partitions,np.round(A_recovered)) # check_degree_sequence can't deal with weighted edges so round

    if correct_degree_sequence:
      adjacency_table = Graph.create_adjacency_table(n,A_recovered)
      multipartite_graph_recognizer=Multipartite_graph_recognizer(partitions,adjacency_table)
      ok=multipartite_graph_recognizer.check()
      print('multipartite:',multipartite_graph_recognizer.match)
    else:
      print('incorrect degree sequence')
      ok=False

    if ok:
     correct_count +=1
  return correct_count

if __name__ == '__main__':
  n=16
  # (8,8) graph
  p=(8,8)
  multipartite_graph_matrix =complete_multipartite(p)

  iterations = 100

  perturbations = [0.2, 0.22,0.25]
  epsilons = [0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.12, 0.15, 0.2, 0.22, 0.25]
  file_path = '../results/multipartite_denoise_epsilon_2.txt'
  f=open(file_path,'w')
  for perturbation in perturbations:
    print('Perturbation scale: ',perturbation)
    for epsilon in epsilons: 
      print('epsilon: ',epsilon)
      correct_count = run_simulation(n,multipartite_graph_matrix,iterations,p,perturbation_scale=perturbation)
    f.write(str(perturbation) + ' ' + str(epsilon) + ' ' + str(correct_count) +'\n')
    print(str(correct_count)+ ' out of '+ str(iterations) + ' iterations, with epsilon =' + str(epsilon))
  f.close()





