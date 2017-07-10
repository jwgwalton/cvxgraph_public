#!/usr/bin/env python3
from itertools import product
import cvxpy as cvx
import numpy as np
from graphs.complement_graph import ComplementGraph

class LovaszCalculator:
  LAMBDA_METHOD = 'lambda'
  TRACE_METHOD = 'trace'

  def __init__(self):
    pass

  def calculate(self, n,edge_locations, solver=cvx.CVXOPT, method=LAMBDA_METHOD):   
    if method == self.TRACE_METHOD:
      problem = self.lovasz_trace(n,edge_locations,solver)
    if method == self.LAMBDA_METHOD:
      problem = self.lovasz_lambda(n,edge_locations,solver)
    else: 
      print('Unknown method, defaulting to using lambda method to calculate ϑ') 
      problem = self.lovasz_lambda(n,edge_locations,solver)

    if problem.status=='optimal':
      return problem.status,problem.value
    else:
      return problem.status,np.nan


  def lovasz_lambda(self, n, edge_locations, solver=cvx.CVXOPT, kktsolver='robust'):
    '''
    Computes lovasz number by

       theta(G) = min lambda_max(A)

     A is defined by 
       a_ij= 1 when i=j  
       or
       a_ij = 1 when i~j not an edge
    '''
    X = cvx.Variable(n,n)
    objective = cvx.Minimize(cvx.lambda_max(X))

    # non-edge locations in the adjacency matrix
    complement_graph_constraints = [X[i,j]==1 for i,j in ComplementGraph.iterator(n,edge_locations)]  

    #A_ij = 1, when i = j
    diagonal_constraints = [X[i,i]==1 for i in range(n)]

    constraints = diagonal_constraints + complement_graph_constraints

    problem = cvx.Problem(objective,constraints)

    #robust kktsolver only works with CVXOPT
    if solver == cvx.CVXOPT:
      problem.solve(solver=solver,kktsolver=kktsolver)  
    else:
      problem.solve(solver=solver)

    return problem


  def lovasz_trace(self, n, edge_locations, solver=cvx.CVXOPT,kktsolver='robust'):
    '''
    Computes lovasz number by

    theta(G) = max Trace(BJ)

    B is defined by
    b_ij = 0 when i~j is an edge

    J is the n*n matrix of ones
    '''

    X = cvx.Variable(n,n)
    J = np.ones((n,n))

    objective = cvx.Maximize(cvx.trace(X*J))

    # edge locations computed in the adjacency matrix
    edge_constraints=            [X[i,j]==0 for i,j in edge_locations]
    edge_constraints_symmetric = [X[j,i]==0 for i,j in edge_locations]

    constraints = [cvx.trace(X) == 1,] + edge_constraints + edge_constraints_symmetric

    problem = cvx.Problem(objective,constraints)

    #robust kktsolver only works with CVXOPT
    if solver == cvx.CVXOPT:
      problem.solve(solver=solver,kktsolver=kktsolver)  
    else:
      problem.solve(solver=solver)

    return problem

if __name__ == '__main__':

  lovasz_calculator = LovaszCalculator()

  # K_4, 4 node complete graph.
  # theta(K_n) = 1  
  n = 4
  edges=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3),)

  status,value = lovasz_calculator.calculate(n,edges,method=lovasz_calculator.TRACE_METHOD)
  print('Problem status ',status)
  print('Lovasz number = %.4g'%(value))

  # K_3, 3 node complete graph
  # theta(K_n) = 1  
  n = 3
  edges=((0,1),(0,2),(1,2),)

  # test lambda method
  status,value = lovasz_calculator.calculate(n,edges,method=lovasz_calculator.LAMBDA_METHOD)
  print('Problem status ',status)
  print('Lovasz number = %.4g'%(value))
