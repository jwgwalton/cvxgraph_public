#!/usr/bin/env python3
import numpy as np
import random
from denoise import GraphDenoiser
from graphs.graph import Graph
from graphs.graph_loader import GraphLoader
from graphs.graph_visualiser import GraphVisualiser
from is_cycle import is_cycle

#############################################################################################
# Test denoiser #
#############################################################################################

def perturb_matrix(n,matrix, perturbation_scale):
  pertubation_matrix = np.random.normal(scale=perturbation_scale,size=(n,n))
  return matrix+pertubation_matrix


def run_simulation(n, cycle,itererations, perturbation_scale = 0.1,epsilon=0):
  correct_count = 0

  graph_denoiser = GraphDenoiser(n,cycle)
  
  A_matrix = Graph.create_adjacency_matrix(n,A)  

  for i in range(0,iterations):
    # perturb matrix (introduce noise to the weights)
    A_matrix_noisy = perturb_matrix(n,A_matrix,perturbation_scale)

    status,problem_value,A_recovered= graph_denoiser.denoise(A_matrix_noisy)

    print('Problem status: ',status)
    cycle = is_cycle(Graph.create_adjacency_list(n,A_recovered))
    print('Is cycle: ', cycle)

    if cycle:
     correct_count +=1
  return correct_count

if __name__ == '__main__':
  n=16

  #16 cycle
  A = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)

  iterations = 100
  graph_name = 'cycle'

  perturbations = [0.15, 0.2, 0.22, 0.25,0.3,0.32,0.35, 0.4, 0.42, 0.45, 0.5 ]
  epsilons = [0, 0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.12, 0.15, 0.2, 0.22, 0.25]
  file_path = 'results/'+graph_name+'_denoise_epsilon3.txt'
  f=open(file_path,'w')
  for perturbation in perturbations:
    print('Perturbation scale: ',perturbation)
    for epsilon in epsilons: 
      print('epsilon: ',epsilon)
      correct_count = run_simulation(n,A,iterations,perturbation_scale=perturbation,epsilon=epsilon)
      f.write(str(perturbation) + ' ' + str(epsilon) + ' ' + str(correct_count) +'\n')
      print(str(correct_count)+ ' out of '+ str(iterations) + ' iterations, with epsilon =' + str(epsilon))
  f.close()
