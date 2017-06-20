#!/usr/bin/env python3
import cvxpy as cvx
from cvxpy.expressions.expression import Expression
import numpy as np

def generate_graph(n, A, constraints):

  np.random.seed(1)
  M = np.random.normal(size=(n,n))

  objective = cvx.Maximize(cvx.trace(M*A))

  problem = cvx.Problem(objective,constraints)

  problem.solve()

  # method to check normal tangent cones, gracefully handle failure

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
  one_vec=np.ones(n)
  degree_constraints = [(1/8)*A*one_vec == one_vec]
 
  # all values between 0 and 1
  limit_constraints = [A>=0,A<=1] 

  # TODO 2nd largest eigenvalue of the laplaciaan >= 4
  #A_const = Expression.cast_to_const(A)
  #degree_matrix = np.diag(np.sum(A_const,1))
  #laplacian_matrix = degree_matrix - A_const
  
  #laplacian_constraints = [np.linalg.eigvalsh(laplacian_matrix)[n-1] >=4]

  # diag(A) == 0
  diagonal_constraints =[]
  for i in range(n):
    diagonal_constraints.append(A[i,i]==0)    

  constraints = limit_constraints + diagonal_constraints + degree_constraints #+ laplacian_constraints

  status,problem_value,graph = generate_graph(n, A, constraints)

  print('Problem status ',status)
  print('Adjacency matric which satisfies constraints: ', np.round(graph,5))
  # trying to be smart and create a set and check content and length to print true false
  print('Degree of nodes : ',np.reshape(np.sum(graph,axis=1),n))
