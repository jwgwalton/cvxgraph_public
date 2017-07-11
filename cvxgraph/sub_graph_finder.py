#!/usr/bin/env python3
import cvxpy as cvx
import numpy as np
from graphs.graph import Graph
from graphs.erdos_renyi_graph import ErdosRenyiGraph
from utils.utils import Utils
from constraints.spectral_hull_constraint import SpectralHullConstraint
from constraints.edge_location_constraint import EdgeLocationConstraint
from collections import Counter

def transform_matrix(n,A_tau,gamma):
  print(A_tau)
  m,k = A_tau.shape
  I = np.identity(k)
  return_matrix = np.zeros((n,n))
  transformed_matrix = A_tau - gamma*I
  return_matrix[0:k,0:k] = transformed_matrix # zero padded the transformed matrix
  #print(return_matrix)
  return return_matrix 


def calculate_gamma(A_tau):
  eigenvalues = np.linalg.eigvalsh(A_tau)
  #print(Counter(eigenvalues))
  values, counts = zip(*Counter(eigenvalues).items())
  #print(values)  
  #print(counts)
  return counts[len(counts)-1] #is this largest one every time (counter returns in order)

def sub_graph_finder(A_tau, A0):
  m,n = A0.shape
  A = cvx.Symmetric(n)
  
  #objective function
  objective = cvx.Maximize(cvx.trace(A*A0)) 

  # A_i,j = 0 if A0_i,j = 0 (and i != j)
  edge_constraints = EdgeLocationConstraint(n,A0,A,0)
  
  # γ =eigenvalue corresponding to the largest eigenspace of the corresponding graph (eigenvalue with highest multiplicity)
  gamma = calculate_gamma(A_tau)

  #TODO SCHUR-HORN CONSTRAINT (semi-definite representation is the same as the spectral hull constraint (but can be reduced for multiplicative eigenvalues)
  schur_horn_constraints = SpectralHullConstraint(transform_matrix(n, A_tau, gamma), A) #doesn't take advantage of the simplifications due to the small numbers of eigenvalues
  
  constraints = edge_constraints.constraint_list + schur_horn_constraints.constraint_list
  
  problem = cvx.Problem(objective,constraints)

  problem.solve()

  if problem.status=='optimal':
    return problem.status,problem.value,A.value
  else:
    return problem.status,np.nan,np.nan

if __name__ == '__main__':

  nk4=4
  K4_A=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3),)
  K4_matrix = Graph.create_adjacency_matrix(nk4,K4_A)


  #Generate large graph with erdos renyi model
  n=40
  p=0.5
  er_graph = ErdosRenyiGraph(n,p)
  network = er_graph.generator() #need to rename doesn't make much sense
  A0 = Graph.create_adjacency_matrix(n,network)

  #embed subgraph (should randomise the location)
  n_2 = 20 #n/2
  A0[n_2:n_2+nk4,n_2:n_2+nk4]=K4_matrix # put in the middle
  sub_graph_finder(K4_matrix,A0)

  status,value,sub_graph_location = sub_graph_finder(K4_matrix,A0)



