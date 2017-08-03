#!/usr/bin/env python3
import cvxpy as cvx
import numpy as np
from constraints.spectral_hull_constraint import SpectralHullConstraint
from constraints.node_limit_constraint import NodeLimitConstraint
from graphs.graph import Graph
from graphs.graph_loader import GraphLoader
from graphs.graph_visualiser import GraphVisualiser
from utils.utils import Utils

class GraphDeconvolver:
  '''
    Recover the precise labelling of the decomposition of A which is an unknown labelling of the convolution of A1 and A2.

    Args:
      n  (int)    : number of nodes/dimension of adjacency matrix
      A1 (tuple) : Component of A 
      A2 (tuple) : Component of A
  '''
  def __init__(self, n, A1, A2):
    self.n = n
    self.A1 = Graph.create_adjacency_matrix(n,A1) #could accept either matrix or tuple and create matrix if needed?
    self.A2 = Graph.create_adjacency_matrix(n,A2)

  def deconvolve(self, A):
    '''
    Recover the precise labelling of A1 and A2, A = A1+A2.

    Args:
      A  (matrix) : Composition of A1 and A2

    Returns:
      problem.status  (str)    : Optimal/
      problem_correct (bool)   : Correctness of solution
      problem.value   (float)  : Value of objective function (Euclidean norm of (A-A1*-A2*))
      A1*             (matrix) : Precise labelling of A1
      A2*             (matrix) : Precise labelling of A2
    '''

    # Realisations of the precise labelling of A1 and A2
    A1_labelled = cvx.Symmetric(self.n)  
    A2_labelled = cvx.Symmetric(self.n)

    # objective function
    objective = cvx.Minimize(cvx.pnorm((A - A1_labelled - A2_labelled), 2))

    # Convex hull constraints
    A1_hull = SpectralHullConstraint(self.A1, A1_labelled)
    A2_hull = SpectralHullConstraint(self.A2, A2_labelled)

    # all values between 0 and 1
    A1_limits = NodeLimitConstraint(A1_labelled,lower_limit=0, upper_limit=1)
    A2_limits = NodeLimitConstraint(A2_labelled,lower_limit=0, upper_limit=1)

    constraints = A1_hull.constraint_list + A2_hull.constraint_list + A1_limits.constraint_list + A2_limits.constraint_list 

    problem = cvx.Problem(objective,constraints)

    problem.solve(solver=cvx.MOSEK)

    if problem.status=='optimal':
      return problem.status,problem.value,A1_labelled.value,A2_labelled.value
    else:
      return problem.status,np.nan,np.nan,np.nan


if __name__ == '__main__':
  n=16
  #  check size(A) = size(A1)+ size(A2)
  A = ((0,1),(0,4),(0,7),(0,9),(0,10),(1,2),(1,5),(1,8),(1,11),(2,3),(2,6),(2,9),(2,12),(3,4),(3,5),(3,7),(3,13),(4,6),(4,8),(4,14),(5,10),(5,14),(5,15),(6,10),(6,11),(6,15),(7,11),(7,12),(7,15),(8,12),(8,13),(8,15),(9,13),(9,14),(9,15),(10,12),(10,13),(11,13),(11,14),(12,14),(0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)
  
  #16 cycle
  A1 = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)

  #clebsch graph
  A2=((0,1),(0,4),(0,7),(0,9),(0,10),(1,2),(1,5),(1,8),(1,11),(2,3),(2,6),(2,9),(2,12),(3,4),(3,5),(3,7),(3,13),(4,6),(4,8),(4,14),(5,10),(5,14),(5,15),(6,10),(6,11),(6,15),(7,11),(7,12),(7,15),(8,12),(8,13),(8,15),(9,13),(9,14),(9,15),(10,12),(10,13),(11,13),(11,14),(12,14),)

  A_matrix = Graph.create_adjacency_matrix(n,A)

  graph_deconvolver = GraphDeconvolver(n,A1,A2)

  status,problem_value,A1_star,A2_star= graph_deconvolver.deconvolve(A_matrix)

  np.set_printoptions(suppress=True)
  print('Problem status: ',status)
  print('Norm value: ',problem_value)
  print('A:  \n', A_matrix)
  print('A1: \n', A1_star)
  print('A2: \n', A2_star)
  print('A1+A2: \n ', np.add(A1_star,A2_star))


  def set_visualiser_attributes(graph_visualiser):
    graph_visualiser.A.node_attr['shape']='circle'
    graph_visualiser.A.node_attr['style']='filled'
    graph_visualiser.A.node_attr['color']='red'
    graph_visualiser.A.edge_attr['color']='blue'
    graph_visualiser.A.edge_attr['penwidth']='2em'
    return graph_visualiser
   
  graph_visualiser = GraphVisualiser(Graph.create_adjacency_list(n,A_matrix))
  graph_visualiser = set_visualiser_attributes(graph_visualiser)
  graph_visualiser.draw_png('figures/A_small.png')

  graph_visualiser = GraphVisualiser(Graph.create_adjacency_list(n,np.round(A1_star)))
  graph_visualiser = set_visualiser_attributes(graph_visualiser)
  graph_visualiser.draw_png('figures/A1_star_small.png')

  graph_visualiser = GraphVisualiser(Graph.create_adjacency_list(n,np.round(A2_star)))
  graph_visualiser = set_visualiser_attributes(graph_visualiser)
  graph_visualiser.draw_png('figures/A2_star_small.png')


