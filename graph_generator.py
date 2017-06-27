#!/usr/bin/env python3
import cvxpy as cvx
import numpy as np
import scipy
from constraints.diagonal_constraint import DiagonalConstraint
from constraints.degree_constraint import DegreeConstraint
from constraints.node_limit_constraint import NodeLimitConstraint
from constraints.laplacian_lambda_second_min_constraint import LaplacianLambdaSecondMinConstraint

def generate_graph(n, A, constraints):

  np.random.seed(1)
  M = np.random.normal(size=(n,n))

  objective = cvx.Maximize(cvx.trace(M*A))

  problem = cvx.Problem(objective,constraints)

  problem.solve(verbose=True)

  # gracefully handle failure or infeasibility?

  if problem.status=='optimal':
    return problem.status,problem.value,A.value

  else:
    return problem.status,np.nan,np.nan

if __name__ == '__main__':

  # 40 degree graph, degree *, second_smallest eigenvalue of lthe laplacian larger than 4
  n=40

  # adjacency matrix of graph
  A = cvx.Symmetric(n)

  # all nodes have degree 8
  degree_constraints = DegreeConstraint(n,A,8)
 
  # all values between 0 and 1
  limit_constraints = NodeLimitConstraint(A,lower_limit=0, upper_limit=1) 

  # 2nd largest eigenvalue of the laplacian >= 4
  laplacian_constraints = LaplacianLambdaSecondMinConstraint(A,4)

  # diag(A) == 0
  diagonal_constraints = DiagonalConstraint(n,A,0) 

  constraints = limit_constraints.constraint_list + diagonal_constraints.constraint_list + degree_constraints.constraint_list + laplacian_constraints.constraint_list

  status,problem_value,graph = generate_graph(n, A, constraints)

  print('Problem status ',status)
  print('Adjacency matric which satisfies constraints: ', np.round(graph,5))
  print('Dimensions of Adjacency matrix: ', np.shape(graph))
 
  laplacian_of_adjacency_matrix = scipy.sparse.csgraph.laplacian(graph)
  sorted_eigen_values = np.linalg.eigvalsh(laplacian_of_adjacency_matrix)
  #print('Eigenvalues of laplacian: ',sorted_eigen_values)
  print('2nd smallest eigenvalue: ', sorted_eigen_values[1])
  # trying to be smart and create a set and check content and length to print true false
  print('Degree of nodes : ',np.reshape(np.sum(graph,axis=1),n))
