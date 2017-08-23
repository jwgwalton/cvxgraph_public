#!/usr/bin/env python3
import numpy as np
import random
from deconvolve import GraphDeconvolver
from graphs.graph import Graph
from graphs.graph_loader import GraphLoader
from graphs.graph_visualiser import GraphVisualiser
from is_cycle import is_cycle
from gaussian_noise_perturb import perturb_matrix

#############################################################################################
# Test pertubing the graph by  adding noise to the edges, (small pertubations in magnitude) #
#############################################################################################

def run_simulation(n, A1, clebsch_graph, iterations, perturbation_scale = 0.1,epsilon=0):
  correct_count = 0
  epsilon_vector = epsilon*np.ones(n)
  for i in range(0,iterations):
    # perturb matrix (introduce noise to the weights)
    clebsch_matrix = perturb_matrix(clebsch_graph.adjacency_matrix, perturbation_scale)
    A2 = Graph.create_adjacency_list(n,clebsch_matrix) #need to do this as it hasn't updated the internal adjacency list representation

    # graph deconvolver with new components
    graph_deconvolver = GraphDeconvolver(n,A1,A2)

    #convolved graphs
    A_matrix  = Graph.create_adjacency_matrix(n,A1) + clebsch_matrix

    status,problem_value,A1_star,A2_star= graph_deconvolver.deconvolve(A_matrix,epsilon_vector)

    if status == 'optimal':
      print('Problem status: ',status)
      cycle = is_cycle(Graph.create_adjacency_list(n,A1_star))
      print('Is cycle: ', cycle)

      if cycle:
        correct_count +=1
  return correct_count

if __name__ == '__main__':
  n=16
  graph_name = 'clebsch'
  # clebsch graph
  file_path = 'graphs/data/'+graph_name+'.txt'
  graph_loader = GraphLoader(n,file_path)
  clebsch_graph = graph_loader.load()

  #16 cycle
  A1 = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)

  iterations = 100

  perturbations = [0.005, 0.0052, 0.0055]#, 0.22, 0.25]
  epsilons = [0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1]
  file_path = 'results/'+graph_name+'_deconvolution_small_perturbation_005_epsilon.txt'
  f=open(file_path,'w')
  for perturbation in perturbations:
    print('Perturbation scale: ',perturbation)
    for epsilon in epsilons: 
      print('epsilon: ',epsilon)
      correct_count = run_simulation(n, A1,clebsch_graph,iterations,perturbation_scale=perturbation,epsilon=epsilon)
      f.write(str(perturbation) + ' ' + str(epsilon) + ' ' + str(correct_count) +'\n')
      print(str(correct_count)+ ' out of '+ str(iterations) + ' iterations, with epsilon =' + str(epsilon))
  f.close()
