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

class GraphDenoiser:
  '''
    Find the graph with noise removed

    Args:
      n  (int)    : number of nodes/dimension of adjacency matrix
      A (tuple) : Adjacency list of A 
  '''
  def __init__(self, n, A):
    self.n = n
    self.A = Graph.create_adjacency_matrix(n,A) #could accept either matrix or tuple and create matrix if needed?

  def denoise(self, A_noisy, epsilon=0):
    A_recovered= cvx.Symmetric(self.n)  

    objective = cvx.Minimize(cvx.pnorm((A_noisy - A_recovered), 2))

    spectral_hull = SpectralHullConstraint(self.A, A_recovered, epsilon=epsilon)
    node_limits = NodeLimitConstraint(A_recovered,lower_limit=0, upper_limit=1)

    constraints = spectral_hull.constraint_list +  node_limits.constraint_list 

    problem = cvx.Problem(objective,constraints)
    problem.solve(solver=cvx.MOSEK)

    if problem.status=='optimal':
      return problem.status,problem.value,A_recovered.value
    else:
      return problem.status,np.nan,np.nan


if __name__ == '__main__':

  n=16
  
  #16 cycle
  A = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),)

  graph_denoiser = GraphDenoiser(n,A)

  # add gaussian noise to cycle
  
  A_matrix = Graph.create_adjacency_matrix(n,A)
  A_matrix_noisy = perturb_matrix(n,A_matrix,0.4)

  status,problem_value,A_recovered= graph_denoiser.denoise(A_matrix_noisy)

  np.set_printoptions(suppress=True)
  print('Problem status: ',status)
  print('Norm value: ',problem_value)
  print('Recovered A:  \n', A_recovered)


  def set_visualiser_attributes(graph_visualiser):
    graph_visualiser.A.node_attr['shape']='circle'
    graph_visualiser.A.node_attr['style']='filled'
    graph_visualiser.A.node_attr['color']='red'
    graph_visualiser.A.edge_attr['color']='blue'
    graph_visualiser.A.edge_attr['penwidth']='2em'
    return graph_visualiser
   

  graph_visualiser = GraphVisualiser(Graph.create_adjacency_list(n,np.ceil(A_matrix_noisy))) # use ceiling so it displays the small ones which would be rounded down
  graph_visualiser = set_visualiser_attributes(graph_visualiser)
  graph_visualiser.draw_png('figures/A_noisy.png')

  graph_visualiser = GraphVisualiser(Graph.create_adjacency_list(n,A_matrix_noisy)) #thresholds within create_adjacency_list
  graph_visualiser = set_visualiser_attributes(graph_visualiser)
  graph_visualiser.draw_png('figures/A_thresholded.png')

  graph_visualiser = GraphVisualiser(Graph.create_adjacency_list(n,A_recovered))
  graph_visualiser = set_visualiser_attributes(graph_visualiser)
  graph_visualiser.draw_png('figures/A_recovered.png')



