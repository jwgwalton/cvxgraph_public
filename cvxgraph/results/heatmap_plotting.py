#!/usr/bin/env python3
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def load_results(file_location):
  results = np.loadtxt(file_location, comments="#", delimiter=" ", unpack=False)
  sigma=[]
  epsilon=[]
  success=[]
  for result in results:
    sigma.append(result[0])
    epsilon.append(result[1])
    success.append(result[2])
  return sigma,epsilon,success


if __name__ == '__main__':
  file_location = 'clebsch_deconvolution_small_perturbation_epsilon.txt'
  sigma,epsilon,success = load_results(file_location)

  fig = plt.figure(figsize=(8, 8))
  ax = fig.add_subplot(1, 1, 1)
  ax.tricontourf(sigma,epsilon,success, 100)

  plt.xlabel('σ of Gaussian noise')
  plt.ylabel('ε')

  save_location='deconvolution_absolute_epsilon.pdf'
  plt.savefig(save_location)


  file_location = 'clebsch_deconvolution_small_perturbation_relative_epsilon.txt'
  sigma,epsilon,success = load_results(file_location)

  fig = plt.figure(figsize=(8, 8))
  ax = fig.add_subplot(1, 1, 1)
  ax.tricontourf(sigma,epsilon,success, 100)

  plt.xlabel('σ of Gaussian noise')
  plt.ylabel('ε')

  save_location='deconvolution_relative_epsilon.pdf'
  plt.savefig(save_location)


  file_location = 'cycle_denoise_epsilon.txt'
  sigma,epsilon,success = load_results(file_location)

  fig = plt.figure(figsize=(8, 8))
  ax = fig.add_subplot(1, 1, 1)
  ax.tricontourf(sigma,epsilon,success, 100)

  plt.xlabel('σ of Gaussian noise')
  plt.ylabel('ε')

  save_location='denoise_epsilon.pdf'
  plt.savefig(save_location)

