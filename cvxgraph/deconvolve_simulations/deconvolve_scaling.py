#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', ))
from graphs.graph import Graph
from graphs.graph_loader import GraphLoader
from graphs.graph_visualiser import GraphVisualiser
from deconvolve import GraphDeconvolver
from eigenvalue_investigations.eigenvalue_permutations import matrix_permute


if __name__ == '__main__':
  n=45
  # regular graph
  file_path = 'graphs/data/45_12_3_3.txt'
  graph_loader = GraphLoader(n,file_path)
  regular_graph = graph_loader.load()

  # randomly permute 
  regular_matrix = matrix_permute(n,regular_graph.adjacency_matrix)
  
  A2 = Graph.create_adjacency_list(n,regular_matrix) #need to do this as it hasn't updated the internal adjacency list representation

  #45 cycle
  A1 = ((0,24),(0,34),(1,10),(1,26),(2,33),(2,41),(3,7),(3,38),(4,28),(4,32),(5,19),(5,23),(6,18),(6,42),(7,16),(8,13),(8,25),(9,36),(9,37),(10,30),(11,13),(11,34),(12,29),(12,39),(14,23),(14,33),(15,25),(15,30),(16,28),(17,24),(17,43),(18,43),(19,22),(20,32),(20,40),(21,35),(21,44),(22,37),(26,40),(27,31),(27,41),(29,42),(31,38),(35,36),(39,44))

  A_matrix  = Graph.create_adjacency_matrix(n,A1) + regular_matrix #convolve the components

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
  graph_visualiser.draw_png('figures/A.png')

  graph_visualiser = GraphVisualiser(Graph.create_adjacency_list(n,np.round(A1_star)))
  graph_visualiser = set_visualiser_attributes(graph_visualiser)
  graph_visualiser.draw_png('figures/A1_star.png')

  graph_visualiser = GraphVisualiser(Graph.create_adjacency_list(n,np.round(A2_star)))
  graph_visualiser = set_visualiser_attributes(graph_visualiser)
  graph_visualiser.draw_png('figures/A2_star.png')

