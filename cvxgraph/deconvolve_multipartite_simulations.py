#!/usr/bin/env python3
import numpy as np
import random
from deconvolve import GraphDeconvolver
from graphs.graph import Graph
from graphs.graph_visualiser import GraphVisualiser
from multipartite_graphs.generate_multipartite_graphs import complete_multipartite
from is_cycle import is_cycle

#####################################################################################
# Test deconvolve complete multipartite graphs #
#####################################################################################

if __name__ == '__main__':
  n=16
  # (8,8) graph
  multipartite_graph =complete_multipartite((8,8))
  A2 = Graph.create_adjacency_list(n,multipartite_graph)

  #16 cycle
  A1 = ((0,5),(5,13),(13,14),(14,6),(6,1),(1,7),(7,2),(2,8),(8,11),(11,15),(15,10),(10,9),(9,4),(4,12),(12,3),(3,0),)
  #multipartite_graph2 =complete_multipartite((4,4,4,4))
  #A1 = Graph.create_adjacency_list(n,multipartite_graph2)

  # graph deconvolver with new components
  graph_deconvolver = GraphDeconvolver(n,A1,A2)

  #convolved graphs
  A_matrix  = Graph.create_adjacency_matrix(n,A1) + multipartite_graph

  status,is_correct,problem_value,A1_star,A2_star= graph_deconvolver.deconvolve(A_matrix)

  np.set_printoptions(suppress=True)
  print('Problem status: ',status)
  print('Problem correct: ', is_correct)
  print('Norm value: ',problem_value)
  cycle = is_cycle(Graph.create_adjacency_list(n,A1_star))
  print('Is cycle: ', cycle)
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
  graph_visualiser.draw_png('figures/A_multipartite.png')

  graph_visualiser = GraphVisualiser(Graph.create_adjacency_list(n,np.round(A1_star)))
  graph_visualiser = set_visualiser_attributes(graph_visualiser)
  graph_visualiser.draw_png('figures/A1_star_multipartite.png')

  graph_visualiser = GraphVisualiser(Graph.create_adjacency_list(n,np.round(A2_star)))
  graph_visualiser = set_visualiser_attributes(graph_visualiser)
  graph_visualiser.draw_png('figures/A2_star_multipartite.png')




