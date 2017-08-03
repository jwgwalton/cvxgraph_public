#!/usr/bin/env python3
import numpy as np
import random
from deconvolve import GraphDeconvolver
from graphs.graph import Graph
from graphs.graph_visualiser import GraphVisualiser
from multipartite_graphs.generate_multipartite_graphs import complete_multipartite
from is_cycle import is_cycle
from degree_sequence import check_degree_sequence
from multipartite_graphs.multipartite_graph_recognizer_00 import Multipartite_graph_recognizer

#####################################################################################
# Test deconvolve complete multipartite graphs with small pertubations #
#####################################################################################

def perturb_matrix(n,matrix, perturbation_scale):
  pertubation_matrix = np.random.normal(scale=perturbation_scale,size=(n,n))
  return matrix+pertubation_matrix


def run_simulation(n, A1, multipartite_graph_matrix, iterations, partitions, perturbation_scale = 0.1):
  correct_count = 0
  for i in range(0,iterations):
    # perturb matrix (introduce noise to the weights)
    graph_matrix = perturb_matrix(n,multipartite_graph_matrix, perturbation_scale)
    A2 = Graph.create_adjacency_list(n,graph_matrix) #need to do this as it hasn't updated the internal adjacency list representation

    # graph deconvolver with new components
    graph_deconvolver = GraphDeconvolver(n,A1,A2)

    #convolved graphs
    A_matrix  = Graph.create_adjacency_matrix(n,A1) + graph_matrix

    status,problem_value,A1_star,A2_star= graph_deconvolver.deconvolve(A_matrix)

    # first check has the correct degree sequence before check multipartite, (needs to be complete)
    correct_degree_sequence = check_degree_sequence(partitions,np.round(A2_star)) # check_degree_sequence can't deal with weighted edges so round

    if correct_degree_sequence:
      adjacency_table = Graph.create_adjacency_table(n,A2_star)
      #print('p=',partitions,'\ng=',adjacency_table)
      multipartite_graph_recognizer=Multipartite_graph_recognizer(partitions,adjacency_table)
      ok=multipartite_graph_recognizer.check()
      print('multipartite:',multipartite_graph_recognizer.match)
    else:
      print('incorrect degree sequence')
      ok=False

    np.set_printoptions(suppress=True)
    print('Problem status: ',status)
    cycle = is_cycle(Graph.create_adjacency_list(n,A1_star))
    print('Is cycle: ', cycle)
    print('A2 correct: ',ok)

    if cycle and ok:
     correct_count +=1
  return correct_count

if __name__ == '__main__':
  n=16
  # (8,8) graph
  p=(8,8)
  multipartite_graph_matrix =complete_multipartite(p)
  A2 = Graph.create_adjacency_list(n,multipartite_graph_matrix )

  #16 cycle
  A1 = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)

  iterations = 100

  perturbations = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.01, 0.12, 0.15, 0.2, 0.22, 0.25]
  file_path = 'results/multipartite_deconvolution_small_perturbation.txt'
  f=open(file_path,'w')
  for perturbation in perturbations:
    print('Perturbation scale: ',perturbation)
    correct_count = run_simulation(n, A1,multipartite_graph_matrix,iterations,p,perturbation_scale=perturbation)
    f.write(str(perturbation) + ' ' + str(correct_count) +'\n')
    print(str(correct_count) + ' out of '+ str(iterations) + ' iterations')
  f.close()







