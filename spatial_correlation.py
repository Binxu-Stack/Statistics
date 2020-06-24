#!/usr/bin/env ovitos

import numpy as np
from ovito.io import import_file
from ovito.data import CutoffNeighborFinder
filename = "min.cfg"
max_r = 5.0
nbins = 10
dr = max_r/float(nbins)
node = import_file(filename)
data = node.source
finder = CutoffNeighborFinder(max_r, data)

atomic_modulus = []
with open("./atomic_nonaffine_modulus.dat",'r') as infile:
    for line in infile:
        atomic_modulus.append(float(line))

atomic_modulus = np.array(atomic_modulus)
mean_atomic_modulus = atomic_modulus.mean()

corr = np.zeros(nbins)
sigma_i = np.zeros(nbins)
sigma_j = np.zeros(nbins)
#number = np.zeros(nbins)
rho = np.zeros(nbins)

for index in range(data.number_of_particles):
    delta_i = atomic_modulus[index] - mean_atomic_modulus
    for neigh in finder.find(index):
        distance = neigh.distance
        ibin = int(distance/dr)
        if ibin >= 10:
            continue
        j = neigh.index
        delta_j = atomic_modulus[j] - mean_atomic_modulus
        corr[ibin] += delta_i*delta_j
        sigma_i[ibin] += delta_i*delta_i
        sigma_j[ibin] += delta_j*delta_j
        #number[ibin] += 1

for ibin in range(nbins):
    rho[ibin] = corr[ibin]/np.sqrt(sigma_i[ibin])/np.sqrt(sigma_j[ibin])
    print((ibin+0.5)*dr,rho[ibin])

