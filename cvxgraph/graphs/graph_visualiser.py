#!/usr/bin/env python3
import pygraphviz as pgv

class GraphVisualiser():
  '''
  Draw graphs from adjacency list using pygraphviz
  '''
 
  def __init__(self, adjacency_list):
    self.adjacency_list=adjacency_list
    self.A = pgv.AGraph()

  def draw_png(self, save_path):
    self.A.add_edges_from(self.adjacency_list)
    self.A.layout(prog='circo')
    self.A.draw(save_path)
    print('Wrote '+save_path)

    

if __name__ == '__main__':
  K_4_list=((0,1),(0,2),(1,2),(0,3),(1,3),(2,3),)
  graph_visualiser = GraphVisualiser(K_4_list)
  graph_visualiser.draw_png('k4.png')
