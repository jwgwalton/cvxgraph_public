#!/usr/bin/env python3
from pertubation_plotting import load_results, plot_results

if __name__ == '__main__':
  file_location = 'clebsch_deconvolution_small_perturbation.txt'
  x,y = load_results(file_location)

  file_location = 'shrikhande_deconvolution_small_perturbation.txt'
  x1,y1 = load_results(file_location)

  figure_location = 'deconvolution_small_perturbation.pdf'
  plot_results(x,y,x1,y1, figure_location, x_axis_title='σ of Gaussian distributed noise',x_is_log=True)

