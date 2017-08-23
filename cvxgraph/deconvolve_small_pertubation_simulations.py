#!/usr/bin/env python3
import numpy as np
import random
from deconvolve import GraphDeconvolver
from graphs.graph import Graph
from graphs.graph_loader import GraphLoader
from graphs.graph_visualiser import GraphVisualiser
from is_cycle import is_cycle
from gaussian_noise_perturb import perturb_matrix

###############################################################################################
# Test perturbing the graph by  adding noise to the edges, (small perturbations in magnitude) #
###############################################################################################

def run_simulation(n, A1, clebsch_graph, iterations, perturbation_scale = 0.1):
  correct_count = 0
  epsilon_vector = np.zeros(n) # no small parameter

  # graph deconvolver with new components
  graph_deconvolver = GraphDeconvolver(n,A1,clebsch_graph.adjacency_list)

  for i in range(0,iterations):
    # perturb matrix (introduce noise to the weights)
    clebsch_matrix = perturb_matrix(clebsch_graph.adjacency_matrix, perturbation_scale)

    #convolved graphs
    A_matrix  = Graph.create_adjacency_matrix(n,A1) + clebsch_matrix

    status,problem_value,A1_star,A2_star= graph_deconvolver.deconvolve(A_matrix, epsilon_vector)

    print('Problem status: ',status)
    cycle = is_cycle(Graph.create_adjacency_list(n,A1_star))
    print('Is cycle: ', cycle)

    if cycle:
     correct_count +=1
  return correct_count

if __name__ == '__main__':
  n=16
  graph_name = 'shrikhande'
  file_path = 'graphs/data/'+graph_name+'.txt'
  graph_loader = GraphLoader(n,file_path)
  clebsch_graph = graph_loader.load()

  #16 cycle
  A1 = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)

  iterations = 100

  perturbations = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.01, 0.12, 0.15, 0.2, 0.22, 0.25]
  file_path = 'results/'+graph_name+'_deconvolution_small_perturbation.txt'
  f=open(file_path,'w')
  for perturbation in perturbations:
    print('Perturbation scale: ',perturbation)
    correct_count = run_simulation(n, A1,clebsch_graph,iterations,perturbation_scale=perturbation)
    f.write(str(perturbation) + ' ' + str(correct_count) +'\n')
    print(str(correct_count) + ' out of '+ str(iterations) + ' iterations')
  f.close()
