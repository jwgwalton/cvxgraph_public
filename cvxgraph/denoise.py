#!/usr/bin/env python3
import cvxpy as cvx
import numpy as np
from constraints.spectral_hull_constraint import SpectralHullConstraint
from constraints.node_limit_constraint import NodeLimitConstraint
from graphs.graph import Graph
from graphs.graph_loader import GraphLoader
from graphs.graph_visualiser import GraphVisualiser
from utils.utils import Utils
from gaussian_noise_perturb import perturb_matrix
from is_cycle import is_cycle

class GraphDenoiser:
  '''
    Find the graph with noise removed

    Args:
      n  (int)    : number of nodes/dimension of adjacency matrix
      A (tuple) : Adjacency list of A 
  '''
  def __init__(self, n, A):
    self.n = n
    self.A = Graph.create_adjacency_matrix(n,A) # could accept either matrix or tuple and create matrix if needed?

  def denoise(self, A_noisy, epsilon_vector):
    A_recovered= cvx.Symmetric(self.n)  

    objective = cvx.Minimize(cvx.pnorm((A_noisy - A_recovered), 2))

    spectral_hull = SpectralHullConstraint(self.A, A_recovered, epsilon_vector)
    node_limits = NodeLimitConstraint(A_recovered,lower_limit=0, upper_limit=1)

    constraints = spectral_hull.constraint_list +  node_limits.constraint_list 

    problem = cvx.Problem(objective,constraints)
    problem.solve(solver=cvx.MOSEK)

    if problem.status=='optimal':
      return problem.status,problem.value,A_recovered.value
    else:
      return problem.status,np.nan,np.nan


if __name__ == '__main__':
  def cycle(n):
    A=np.zeros((n,n))
    for i in range(n-1): A[i,i+1]=A[i+1,i]=1
    A[0,n-1]=A[n-1,0]=1
    return A

  def bicycle(n):
    A=cycle(n)
    A[0,n//2]=A[n//2,0]=1
    return A

  n=16
  
  #16 cycle
 # A = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)

  #clebsch graph
  A=((0,1),(0,4),(0,7),(0,9),(0,10),(1,2),(1,5),(1,8),(1,11),(2,3),(2,6),(2,9),(2,12),(3,4),(3,5),(3,7),(3,13),(4,6),(4,8),(4,14),(5,10),(5,14),(5,15),(6,10),(6,11),(6,15),(7,11),(7,12),(7,15),(8,12),(8,13),(8,15),(9,13),(9,14),(9,15),(10,12),(10,13),(11,13),(11,14),(12,14),)

  #A_matrix =  bicycle(n)
  #A = Graph.create_adjacency_list(n,A_matrix)

  graph_denoiser = GraphDenoiser(n,A)

  # add gaussian noise to cycle
  
  A_matrix = Graph.create_adjacency_matrix(n,A)
  A_matrix_noisy = perturb_matrix(A_matrix,0.2)

  epsilon_vector = np.zeros(n)

  status,problem_value,A_recovered= graph_denoiser.denoise(A_matrix_noisy, epsilon_vector)

  np.set_printoptions(precision=1e-3,suppress=True)
  print('Problem status: ',status)
  print('Norm value: ',problem_value)
  print('Recovered A:  \n', A_recovered)
  print('is cycle graph: ',is_cycle(Graph.create_adjacency_list(n,A_recovered)))


  def set_visualiser_attributes(graph_visualiser):
    graph_visualiser.A.node_attr['shape']='circle'
    graph_visualiser.A.node_attr['style']='filled'
    graph_visualiser.A.node_attr['color']='red'
    graph_visualiser.A.edge_attr['color']='blue'
    #graph_visualiser.A.edge_attr['penwidth']='2em'
    return graph_visualiser
   

  graph_visualiser = GraphVisualiser(Graph.create_weighted_adjacency_list(n,A_matrix_noisy,1e-6)) # weighted adjacency list
  graph_visualiser = set_visualiser_attributes(graph_visualiser)
  graph_visualiser.draw_png_weighted_graph('figures/A_noisy.png')

  graph_visualiser = GraphVisualiser(Graph.create_adjacency_list(n,A_matrix_noisy)) #thresholds within create_adjacency_list
  graph_visualiser = set_visualiser_attributes(graph_visualiser)
  graph_visualiser.draw_png('figures/A_thresholded.png')

  graph_visualiser = GraphVisualiser(Graph.create_adjacency_list(n,A_recovered))
  graph_visualiser = set_visualiser_attributes(graph_visualiser)
  graph_visualiser.draw_png('figures/A_recovered.png')



