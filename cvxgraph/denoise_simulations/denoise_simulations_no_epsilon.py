#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', ))
import numpy as np
import random
from denoise import GraphDenoiser
from graphs.graph import Graph
from graphs.graph_loader import GraphLoader
from graphs.graph_visualiser import GraphVisualiser
from is_cycle import is_cycle
from gaussian_noise_perturb import perturb_matrix
from generate_epsilon import mean_shift_eigenvalue_distribution

#############################################################################################
# Test denoiser #
#############################################################################################

def calculate_epsilon_vector(matrix, perturbed_matrix):
  original_eigenvalues, o_matrix = eigh(matrix)
  diagonal_eigenvalue_matrix = o_matrix.T*perturbed_matrix*o_matrix
  return np.diag(diagonal_eigenvalue_matrix)

def run_simulation(n, cycle,itererations, perturbation_scale = 0.1):

  correct_count = 0

  graph_denoiser = GraphDenoiser(n,cycle)
  
  A_matrix = Graph.create_adjacency_matrix(n,A)  

  # generate cum sum of mean shift in eigenvalue distribution 


  for i in range(0,iterations):
    # perturb matrix (introduce noise to the weights)
    A_matrix_noisy = perturb_matrix(A_matrix,perturbation_scale)

    epsilon_vector = calculate_epsilon_vector(A_matrix,A_matrix_noisy)
    print

    status,problem_value,A_recovered= graph_denoiser.denoise(A_matrix_noisy,epsilon_vector)

    print('Problem status: ',status)
    cycle = is_cycle(Graph.create_adjacency_list(n,A_recovered))
    print('Is cycle: ', cycle)

    if cycle:
     correct_count +=1
  return correct_count

if __name__ == '__main__':
  n=16

  #16 cycle
 # A = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),)

  #clebsch graph
  A=((0,1),(0,4),(0,7),(0,9),(0,10),(1,2),(1,5),(1,8),(1,11),(2,3),(2,6),(2,9),(2,12),(3,4),(3,5),(3,7),(3,13),(4,6),(4,8),(4,14),(5,10),(5,14),(5,15),(6,10),(6,11),(6,15),(7,11),(7,12),(7,15),(8,12),(8,13),(8,15),(9,13),(9,14),(9,15),(10,12),(10,13),(11,13),(11,14),(12,14),)

  iterations = 100
  graph_name = 'clebsch'

  perturbations = [0.1]#, 0.12, 0.15, 0.2, 0.22, 0.25, 0.3, 0.32, 0.35, 0.4, 0.42, 0.45, 0.5 ]
  file_path = '../results/'+graph_name+'_denoise_pre_calc_epsilon_01.txt'
  f=open(file_path,'w')
  for perturbation in perturbations:
    correct_count = run_simulation(n,A,iterations,perturbation_scale=perturbation)
    f.write(str(perturbation) + ' ' + str(correct_count) +'\n')
    print(str(correct_count)+ ' out of '+ str(iterations) + ' iterations, with pertubation =' + str(perturbation))
  f.close()
