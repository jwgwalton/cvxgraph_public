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

#############################################################################################
# Test denoiser with bicycle #
#############################################################################################

sqrt2 = 1.41421356237

def cycle(n):
  A=np.zeros((n,n))
  for i in range(n-1): A[i,i+1]=A[i+1,i]=1
  A[0,n-1]=A[n-1,0]=1
  return A

def bicycle(n):
  A=cycle(n)
  A[0,n//2]=A[n//2,0]=1
  return A

def run_simulation(n, cycle,itererations, perturbation_scale = 0.1,epsilon=0):
  correct_count = 0

  graph_denoiser = GraphDenoiser(n,cycle)
  
  A_matrix = Graph.create_adjacency_matrix(n,A)  

  # vector of small parameters for spectral hull
  epsilon_vector = epsilon*np.ones(n)

  for i in range(0,iterations):
    # perturb matrix (introduce noise to the weights)
    A_matrix_noisy = perturb_matrix(A_matrix,perturbation_scale)

    status,problem_value,A_recovered= graph_denoiser.denoise(A_matrix_noisy,epsilon_vector)

    if status == 'optimal':
      print('Problem status: ',status)
      cycle = is_cycle(Graph.create_adjacency_list(n,A_recovered))
      print('Is cycle: ', cycle)

      if cycle:
        correct_count +=1
  return correct_count

if __name__ == '__main__':
  n=16

  #16 cycle
  A = Graph.create_adjacency_list(n,bicycle(n))

  iterations = 100
  graph_name = 'bicycle'

  perturbations = [0.05, 0.052, 0.055]
  epsilons = [0, 0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.12, 0.15, 0.2, 0.22, 0.25]
  file_path = '../results/'+graph_name+'_denoise_epsilon_05.txt'
  f=open(file_path,'w')
  for perturbation in perturbations:
    print('Perturbation scale: ',perturbation)
    for epsilon in epsilons: 
      print('epsilon: ',epsilon)
      correct_count = run_simulation(n,A,iterations,perturbation_scale=perturbation,epsilon=epsilon)
      f.write(str(perturbation) + ' ' + str(epsilon) + ' ' + str(correct_count) +'\n')
      print(str(correct_count)+ ' out of '+ str(iterations) + ' iterations, with epsilon =' + str(epsilon))
  f.close()
