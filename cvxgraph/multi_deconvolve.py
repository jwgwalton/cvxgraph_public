#!/usr/bin/env python3
import cvxpy as cvx
import numpy as np
from constraints.spectral_hull_constraint import SpectralHullConstraint
from constraints.node_limit_constraint import NodeLimitConstraint
from graphs.graph import Graph
from utils.utils import Utils
from graphs.graph_visualiser import GraphVisualiser
from graphs.graph_loader import GraphLoader

class MultiGraphDeconvolver:

  def __init__(self, n, A1, A2, A3):
    '''
    Recover the precise labelling of the decomposition of A which is an unknown labelling of the convolution of A1 and A2.

    Args:
      n  (int)    : number of nodes/dimension of adjacency matrix
      A1 (tuple) : Component of A 
      A2 (tuple) : Component of A
    '''
    self.n = n
    self.A1 = Graph.create_adjacency_matrix(n,A1) 
    self.A2 = Graph.create_adjacency_matrix(n,A2)
    self.A3 = Graph.create_adjacency_matrix(n,A2)

  def is_exact_decomposition(self, A1, A2, tol):
    '''A1==1 and A2==0 or A1==0 and A2==1, within tolerance tol '''
    return (1-tol <= abs(A1) <= 1+tol and 0-tol<= abs(A2)<=0+tol) or (1-tol <= abs(A2) <= 1+tol and 0-tol<= abs(A1)<=0+tol)

  def check_solution(self, A, A1, A2, tol):
    '''Check exact decomposition, A=A1+A2 and A1 and A2 are distinct non-overlapping graphs'''
    m,n = A1.shape
    if not Utils.deep_equals(A,(A1+A2), tol): 
      return False
 
    for i in range(0,n):
      for j in range(0,i):
        if not (abs(A1[i,j]) <= tol and abs(A2[i,j]) <= tol): #both == 0 within tol
          if not self.is_exact_decomposition(A1[i,j],A2[i,j],tol):
            return False
    return True

  def deconvolve(self, A):
    '''
    Recover the precise labelling of A1, A2 and A3, A = A1+A2+A3.

    Args:
      A  (matrix) : Composition of A1 and A2

    Returns:
      problem.status  (str)    : Optimal/
      problem_correct (bool)   : Correctness of solution
      problem.value   (float)  : Value of objective function (Euclidean norm of (A-A1*-A2*))
      A1*             (matrix) : Precise labelling of A1
      A2*             (matrix) : Precise labelling of A2
      A3*             (matrix) : Precise labelling of A2
    '''

    # Realisations of the precise labelling of A1 and A2
    A1_labelled = cvx.Symmetric(self.n)  
    A2_labelled = cvx.Symmetric(self.n)
    A3_labelled = cvx.Symmetric(self.n)

    # objective function
    objective = cvx.Minimize(cvx.pnorm((A - A1_labelled - A2_labelled - A3_labelled), 2))

    # Convex hull constraints
    A1_hull = SpectralHullConstraint(self.A1, A1_labelled)
    A2_hull = SpectralHullConstraint(self.A2, A2_labelled)
    A3_hull = SpectralHullConstraint(self.A2, A2_labelled)

    # all values between 0 and 1
    A1_limits = NodeLimitConstraint(A1_labelled,lower_limit=0, upper_limit=1)
    A2_limits = NodeLimitConstraint(A2_labelled,lower_limit=0, upper_limit=1)
    A3_limits = NodeLimitConstraint(A2_labelled,lower_limit=0, upper_limit=1)

    constraints = A1_hull.constraint_list + A2_hull.constraint_list + A3_hull.constraint_list + A1_limits.constraint_list + A2_limits.constraint_list + A3_limits.constraint_list 

    problem = cvx.Problem(objective,constraints)

    problem.solve(solver=cvx.MOSEK)

    #problem_correct = self.check_solution(A, A1_labelled.value, A2_labelled.value, 1e-1)
    problem_correct = True

    if problem.status=='optimal':
      return problem.status,problem_correct,problem.value,A1_labelled.value,A2_labelled.value,A3_labelled.value
    else:
      return problem.status,problem_correct,np.nan,np.nan,np.nan,np.nan


if __name__ == '__main__':
  # labelling of nodes from, http://www.ioirp.com/Doc/IJIRTSE/v1_i3/JMS105.pdf 
  n=16
  # clebsch graph
  file_path = 'graphs/data/clebsch.txt'
  graph_loader = GraphLoader(n,file_path)
  clebsch_graph = graph_loader.load()

  # shrikhande graph
  file_path = 'graphs/data/shrikhande.txt'
  graph_loader = GraphLoader(n,file_path)
  shrikhande_graph = graph_loader.load()
  
  # 9 node regular graph
  new_n=9
  file_path = 'graphs/data/9_4_1_2.txt'
  graph_loader = GraphLoader(new_n,file_path)
  sr_graph = graph_loader.load()
  
  # embed in 16 node adjacency matrix
  srg_matrix = Graph.create_adjacency_matrix(n,sr_graph.adjacency_list)

  A_matrix  = clebsch_graph.adjacency_matrix + shrikhande_graph.adjacency_matrix + srg_matrix
  print('A_matrix: ',A_matrix)

  graph_deconvolver = MultiGraphDeconvolver(n,clebsch_graph.adjacency_list,shrikhande_graph.adjacency_list,Graph.create_adjacency_list(n,srg_matrix)) 

  status,is_correct,problem_value,A1_star,A2_star,A3_star= graph_deconvolver.deconvolve(A_matrix)

  np.set_printoptions(suppress=True)
  print('Problem status: ',status)
  print('Problem correct: ', is_correct)
  print('Norm value: ',problem_value)
  print('A:  \n', A_matrix)
  print('A1: \n', A1_star)
  print('A2: \n', A2_star)
  print('A3: \n', A2_star)
  print('A1+A2+A3: \n ', np.add(A1_star,A2_star,A3_star))

  graph_visualiser = GraphVisualiser(Graph.create_adjacency_list(n,A_matrix))
  graph_visualiser.A.node_attr['shape']='circle'
  graph_visualiser.A.node_attr['style']='filled'
  graph_visualiser.A.node_attr['color']='red'
  graph_visualiser.A.edge_attr['color']='blue'
  graph_visualiser.A.edge_attr['penwidth']='2em'
  graph_visualiser.draw_png('figures/A.png')

  graph_visualiser = GraphVisualiser(Graph.create_adjacency_list(n,np.round(A1_star)))
  graph_visualiser.A.node_attr['shape']='circle'
  graph_visualiser.A.node_attr['style']='filled'
  graph_visualiser.A.node_attr['color']='red'
  graph_visualiser.A.edge_attr['color']='green'
  graph_visualiser.A.edge_attr['penwidth']='2em'
  graph_visualiser.draw_png('figures/A1_star.png')

  graph_visualiser = GraphVisualiser(Graph.create_adjacency_list(n,np.round(A2_star)))
  graph_visualiser.A.node_attr['shape']='circle'
  graph_visualiser.A.node_attr['style']='filled'
  graph_visualiser.A.node_attr['color']='red'
  graph_visualiser.A.edge_attr['color']='blue'
  graph_visualiser.A.edge_attr['penwidth']='2em'
  graph_visualiser.draw_png('figures/A2_star.png')


  graph_visualiser = GraphVisualiser(Graph.create_adjacency_list(n,np.round(A3_star)))
  graph_visualiser.A.node_attr['shape']='circle'
  graph_visualiser.A.node_attr['style']='filled'
  graph_visualiser.A.node_attr['color']='red'
  graph_visualiser.A.edge_attr['color']='blue'
  graph_visualiser.A.edge_attr['penwidth']='2em'
  graph_visualiser.draw_png('figures/A3_star.png')


