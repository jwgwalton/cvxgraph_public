import numpy as np
from scipy.linalg import eigvalsh
from gaussian_noise_perturb import perturb_matrix

def mean_shift_eigenvalue_distribution(graph_matrix, sigma):
  n=graph_matrix.shape[0]
  means=np.zeros(n)

  original_eigenvalues=eigvalsh(graph_matrix)
  iterations = 1000
  for iteration in range(iterations):
    eigenvalues=eigvalsh(perturb_matrix(graph_matrix,sigma))-original_eigenvalues
    means+=(eigenvalues-means)/(1.0+iteration)
  return np.cumsum(means)
