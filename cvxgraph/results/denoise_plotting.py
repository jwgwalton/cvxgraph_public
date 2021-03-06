#!/usr/bin/env python3
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from collections import Counter

def plot_results(x,y,x1,y1,save_location,x_axis_title='σ of Gaussian perturbations',x_is_log=True):
  fig = plt.figure(figsize=(8, 8))
  ax = fig.add_subplot(1, 1, 1)
  if x_is_log:
    ax.set_xscale('log')
  clebsch = plt.scatter(x,y,c='r',marker='x',s=50, label='Cycle')
  shrikhande = plt.scatter(x1,y1,c='b',marker='H',s=50, label='Bicycle')

  plt.xlabel(x_axis_title,fontsize=20)
  plt.ylabel('% success',fontsize=20)
  plt.grid(True)

  plt.legend(handles=[clebsch,shrikhande])

  plt.savefig(save_location)
  plt.close()

def load_results(file_location):
  results = np.loadtxt(file_location, comments="#", delimiter=" ", unpack=False)
  x=[]
  y=[]
  for result in results:
    x.append(result[0])
    y.append(result[2])
  return x,y


if __name__ == '__main__':
  file_location = 'cycle_denoise_no_epsilon.txt'
  x,y = load_results(file_location)

  file_location = 'bicycle_denoise_no_epsilon.txt'
  x1,y1 = load_results(file_location)

  figure_location = 'figures/denoise.pdf'
  plot_results(x,y,x1,y1, figure_location)

