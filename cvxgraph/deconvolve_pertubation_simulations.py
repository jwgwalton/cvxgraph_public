#!/usr/bin/env python3
import numpy as np
import random
from deconvolve import GraphDeconvolver
from graphs.graph import Graph
from graphs.graph_loader import GraphLoader
from eigenvalue_investigations.eigenvalue_pertubations import perturb_matrix
from is_cycle import is_cycle

#####################################################################################
# Test perturbing the graphs by adding removing edges in the strongly regular graph #
#####################################################################################
def run_simulation(n, A1, clebsch_graph, iterations,number_of_pertubations):
  correct_count = 0
  for i in range(0,iterations):
    # perturb matrix (add/remove edge randomly)
    clebsch_matrix = clebsch_graph.adjacency_matrix.copy()
    clebsch_matrix = perturb_matrix(n,clebsch_matrix, number_of_pertubations)
    A2 = Graph.create_adjacency_list(n,clebsch_matrix) #need to do this as it hasn't updated the internal adjacency list representation

    # graph deconvolver with new components
    graph_deconvolver = GraphDeconvolver(n,A1,A2)

    #convolved graphs
    A_matrix  = Graph.create_adjacency_matrix(n,A1) + clebsch_matrix

    status,problem_value,A1_star,A2_star= graph_deconvolver.deconvolve(A_matrix)

    print('Problem status: ',status)
    cycle = is_cycle(Graph.create_adjacency_list(n,A1_star))
    print('Is cycle: ', cycle)

    if cycle:
     correct_count +=1
  return correct_count

if __name__ == '__main__':
  n=16
  graph_name = 'shrikhande'
  # clebsch graph
  file_path = 'graphs/data/'+graph_name+'.txt'
  graph_loader = GraphLoader(n,file_path)
  clebsch_graph = graph_loader.load()

  #16 cycle
  A1 = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)

  iterations = 100
  max_number_perturbations = 4

  file_path = 'results/'+graph_name+'_deconvolution_perturbations.txt'
  f=open(file_path,'w')

  for number_of_perturbations in range(1,max_number_perturbations+1):
    correct_count = run_simulation(n, A1,clebsch_graph,iterations, number_of_perturbations)
    f.write(str(number_of_perturbations) + ' ' + str(correct_count) +'\n')
    print(str(correct_count) + ' out of '+ str(iterations) + ' iterations')
  f.close()



