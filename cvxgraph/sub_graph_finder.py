#!/usr/bin/env python3
import cvxpy as cvx
import numpy as np
from graphs.graph import Graph
from utils import Utils
from constraints.spectral_hull_constraint import SpectralHullConstraint

def transform_matrix(n,A_tau,gamma):
  m,k = A_tau.shape
  I = np.identity(k)
  return A_tau - gamma*I

def calculate_schur_horn_constraints(transformed_matrix):
  
  #SH constraints for transformed_matrix
  return []

def sub_graph_finder(A_tau, A0):
  m,n = A0.shape
  A = cvx.Symmetric(n)
  
  #objective function
  objective = cvx.Maximise(A*A0)

  edge_constraints =[]
  for i in range(0,n):
    for j in range(0,j):
      if A0 == 0: #don't think i need to say and i != j, it's not a multigraph so it's 0 on the diagonal anyway
        edge_constraints += [A[i,j] ==0] #dont need to do symmetric equivalent as A is a symmetric variable
  
  #FIXME γ equal to the eigenvalue corresponding to the largest eigenspace of the corresponding graph (eigenvalue with highest multiplicity)
  # (USE COUNTER CLASS AND CALCULATE FROM EIGENVALUES OF A0)
  gamma = 1

  #TODO SCHUR-HORN CONSTRAINT (semi-definite representation is the same as the spectral hull constraint (but can be reduced for multiplicative eigenvalues)
  schur_horn_constraints = calculate_schur_horn_constraints(transform_matrix(n, A_tau, gamma))
  
  constraints = edge_constraints + schur_horn_constraints
  
  problem = cvx.Problem(objective,constraints)

  problem.solve()

  if problem.status=='optimal':
    return problem.status,problem.value,A.value
  else:
    return problem.status,np.nan,np.nan

