#!/usr/bin/env python3
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter

def plot_results(results,save_location):
  labels, values = zip(*Counter(results).items())
  sum_of_values = sum(values)
  values1 =[value/sum_of_values for value in values] #map to probablities
  print(labels)
  print(values)
 
  fig = plt.figure(figsize=(8, 8))
  ax = fig.add_subplot(1, 1, 1)
  plt.scatter(labels,values1,c='r',marker='x',s=50)

  plt.xlabel('Norm of difference of eigenvalues',fontsize=20)
  plt.ylabel('Probability',fontsize=20)
  plt.grid(True)

  plt.savefig(save_location)
  plt.close()

def plot_graph(graph_name):
  file_location = 'results/'+graph_name+'_eigenvalues.txt'
  figure_location='figures/'+graph_name+'_eigenvalues.pdf'

  results = np.loadtxt(file_location, comments="#", delimiter=",", unpack=False)
  plot_results(results, figure_location)

if __name__ == '__main__':
  plot_graph('clebsch')
  plot_graph('shrikhande')
  plot_graph('17_8_3_4')
  plot_graph('64_18_2_6')
  plot_graph('9_4_1_2')



