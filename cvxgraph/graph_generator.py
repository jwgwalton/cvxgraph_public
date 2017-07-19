#!/usr/bin/env python3
import cvxpy as cvx
import numpy as np
import scipy
from constraints.diagonal_constraint import DiagonalConstraint
from constraints.degree_constraint import DegreeConstraint
from constraints.node_limit_constraint import NodeLimitConstraint
from constraints.laplacian_lambda_second_min_constraint import LaplacianLambdaSecondMinConstraint
from graphs.graph_visualiser import GraphVisualiser
from graphs.graph import Graph

class GraphGenerator:

  def __init__(self,n):
    self.n=n
    self.A=cvx.Symmetric(n)
    np.random.seed(1) # move out of class?
    self.M = np.random.normal(size=(n,n))

  def generate_graph(self, constraints):
    objective = cvx.Maximize(cvx.trace(self.M*self.A))

    problem = cvx.Problem(objective,constraints)

    problem.solve(verbose=True)

    # gracefully handle failure or infeasibility?

    if problem.status=='optimal':
      return problem.status,problem.value,self.A.value
    else:
      return problem.status,np.nan,np.nan

if __name__ == '__main__':
  # 40 degree graph, degree *, second_smallest eigenvalue of the laplacian larger than 4
  n=40

  graph_generator = GraphGenerator(n)

  # all nodes have degree 8
  degree_constraints = DegreeConstraint(n,graph_generator.A,8)
 
  # all values between 0 and 1
  limit_constraints = NodeLimitConstraint(graph_generator.A,lower_limit=0, upper_limit=1) 

  # 2nd largest eigenvalue of the laplacian >= 4
  laplacian_constraints = LaplacianLambdaSecondMinConstraint(graph_generator.A,4)

  # diag(A) == 0
  diagonal_constraints = DiagonalConstraint(n,graph_generator.A,0) 

  constraints = limit_constraints.constraint_list + diagonal_constraints.constraint_list + degree_constraints.constraint_list + laplacian_constraints.constraint_list

  status,problem_value,graph = graph_generator.generate_graph(constraints)

  np.set_printoptions(suppress=True)
  print('Problem status ',status)
  print('Adjacency matrix which satisfies constraints: ', np.round(graph,5)) 
  laplacian_of_adjacency_matrix = scipy.sparse.csgraph.laplacian(graph)
  sorted_eigen_values = np.linalg.eigvalsh(laplacian_of_adjacency_matrix)
  print('2nd smallest eigenvalue: ', sorted_eigen_values[1])
  print('Degree of nodes : ',np.reshape(np.sum(graph,axis=1),n))
  adjacency_list = Graph.create_adjacency_list(n,graph)
  graph_visualiser = GraphVisualiser(adjacency_list)

  graph_visualiser.A.node_attr['shape']='circle'
  graph_visualiser.A.node_attr['style']='filled'
  graph_visualiser.A.node_attr['color']='red'

  graph_visualiser.draw_png('generated_graph.png')
