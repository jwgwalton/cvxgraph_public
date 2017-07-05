#!/usr/bin/env python3
import cvxpy as cvx
import numpy as np
from constraints.spectral_hull_constraint import SpectralHullConstraint
from constraints.node_limit_constraint import NodeLimitConstraint
from graphs.graph import Graph
from utils import Utils

class GraphDeconvolver():

  def __init__(self, n, A1, A2):
    '''
    Recovers the precise labelling of the decomposition of A which is an unknown labelling of the convolution of A1 and A2.

    Args:
      n  (int)    : number of nodes/dimension of adjacency matrix
      A1 (tuple) : Component of A 
      A2 (tuple) : Component of A

    '''
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
      problem_correct (bool)   : Correctness of solution using internal method
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

    problem.solve(kktsolver='robust')

    problem_correct = self.check_solution(A, A1_labelled.value, A2_labelled.value, 1e-2)

    if problem.status=='optimal':
      return problem.status,problem_correct,problem.value,A1_labelled.value,A2_labelled.value
    else:
      return problem.status,problem_correct,np.nan,np.nan,np.nan

  def check_solution(self, A, A1, A2, tol):
    '''
    Checks returns exact decomposition,
    i.e returns integers for the distinct edges and both graphs are separate
    '''
    m,n = A1.shape
    #Check A=A1+A2
    if not (Utils.deep_equals(A,A1+A2)):
      return False

    for i in range(0,n):
      for j in range(0,i):
        if not self.is_exact_decomposition(A1[i,j],A2[i,j],tol) or not self.is_exact_decomposition(A2[i,j],A1[i,j],tol) or not self.is_empty(A1[i,j],A2[i,j]):
          return False
    return True

  def is_exact_decomposition(self, A1, A2, tol):
    '''A1==1 and A2==0, within tolerance tol'''
    return 1-tol <= A1 <= 1+tol and 0-tol<= A2<=0+tol

  def is_empty(self, A1, A2):
    return (A2 == A1 == 0)


if __name__ == '__main__':
  # A= K_4
  n = 4
  A=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3),)

  # A1 = cycle 
  A1=((0,1),(1,2),(2,3),(3,0),)

  # A2 = cross joining all nodes
  A2=((0,2),(1,3),)

  A_matrix  = Graph.create_adjacency_matrix(n,A)

  graph_deconvolver = GraphDeconvolver(n,A1,A2)

  status,is_correct,problem_value,A1_star,A2_star= graph_deconvolver.deconvolve(A_matrix)

  np.set_printoptions(suppress=True)
  print('Problem status: ',status)
  print('Problem correct: ', is_correct)
  print('Norm value: ',problem_value)
  print('A:  \n', A_matrix)
  print('A1: \n', A1_star)
  print('A2: \n', A2_star)
  print('A1+A2: \n ', np.add(A1_star,A2_star))

