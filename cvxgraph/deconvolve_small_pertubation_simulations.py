#!/usr/bin/env python3
import numpy as np
import random
from deconvolve import GraphDeconvolver
from graphs.graph import Graph
from graphs.graph_loader import GraphLoader
from graphs.graph_visualiser import GraphVisualiser
from is_cycle import is_cycle

#############################################################################################
# Test pertubing the graph by  adding noise to the edges, (small pertubations in magnitude) #
#############################################################################################

def perturb_matrix(n,matrix, pertubation_scale):
  pertubation_matrix = np.random.normal(scale=pertubation_scale,size=(n,n))
  return matrix+pertubation_matrix


def run_simulation(n, A1, clebsch_graph, iterations, pertubation_scale = 0.1):
  correct_count = 0
  for i in range(0,iterations):
    # perturb matrix (introduce noise to the weights)
    clebsch_matrix = perturb_matrix(n,clebsch_graph.adjacency_matrix, pertubation_scale)
    A2 = Graph.create_adjacency_list(n,clebsch_matrix) #need to do this as it hasn't updated the internal adjacency list representation

    # graph deconvolver with new components
    graph_deconvolver = GraphDeconvolver(n,A1,A2)

    #convolved graphs
    A_matrix  = Graph.create_adjacency_matrix(n,A1) + clebsch_matrix

    status,is_correct,problem_value,A1_star,A2_star= graph_deconvolver.deconvolve(A_matrix)

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

  smallest_perturbation_scale = 1
  largest_perturbation_scale = 40
  normalisation_scale = 100
  file_path = 'results/'+graph_name+'_deconvolution_small_perturbation.txt'
  f=open(file_path,'w')
  for perturbation_scale in range(smallest_perturbation_scale, largest_perturbation_scale):
    perturbation_scale2 = perturbation_scale/normalisation_scale # can't iterate over non integers
    print('Pertubation scale: ',perturbation_scale2)
    correct_count = run_simulation(n, A1,clebsch_graph,iterations,perturbation_scale2)
    f.write(str(perturbation_scale2) + ' ' + str(correct_count) +'\n')
    print(str(correct_count) + ' out of '+ str(iterations) + ' iterations')
  f.close()

