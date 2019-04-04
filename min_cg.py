#!/usr/bin/env ovitos
# -*- coding: utf-8 -*-
r"""Scipt to calculate the augular-dependent radial distribution function g(r,theta).

Formular:

$g(r,\theta) = \frac{L^3}{2r^2\Delta r \Delta \theta N (N-1)} \Sum_{i \neq j} \delta(r-|r_{ik}) \delta(\theta-\theta_{ik})$,

where \theta is defined with respect to the flow direction (default positive x-direction),
L is the size of box, r is the radial distance, N is the total number of atoms is box.

Reference:

Ingebrigtsen, T. S., Tanaka, H. (2017), 
Structural predictor for nonlinear sheared dynamics in simple glass-forming liquids,
Proceedings of the National Academy of Sciences, 115(1), 201711655.
https://doi.org/10.1073/pnas.1711655115

"""
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# Python template written by Bin Xu (xubinrun@gmail.com)
# Licensed under GPL License

# sys library is often used

import argparse
#import os
#import re
import sys
import numpy as np
import time
#import pandas as pd
import matplotlib.pyplot as plt
#import doctest
#It's a good habit to write testing code.


def min_cg(values, filename='dump.lammpstrj', cutoff=2.0):
    """
    Parameters:

        filename: filename of a configuration, use ASE package to read the positions of atoms,
        so the format should be supported by ASE. Default format: lammps-dump

        cutoff: maximum distance to do min coarse grain, default: 2.0

    Return:
        results: shape(N), the results array.
    """
    from ovito.io import import_file
    from ovito.data import CutoffNeighborFinder
    #from ase.io import read
    node = import_file(filename,multiple_frames = False)
    #atoms = read(filename,format=format)
    data = node.source
    #atoms.set_pbc(True)

    # number of atoms
    N = data.number_of_particles # number of atoms
    print("Number of atoms:",N)

    # volume of cell
    cell = data.cell
    volume = abs(np.linalg.det(cell.matrix[0:3,0:3]))
    #volume = atoms.get_volume()
    print("Volume of cell:",volume)

    # get the bonds 
    #finder = NearestNeighborFinder(N, data)
    finder = CutoffNeighborFinder(max_r, data)

    s = []
    min_results = []
    with open(values, 'r') as instream:
        for line in instream:
            s.append(np.double(line))
            min_results.append(np.double(line))



    # initialize the count matirx, and results matrix
    #min_results = [np.inf]*N

    # test g(r)
    #g = np.zeros(nr_bins+1)
    node.compute()
    atoms_ids = node.outpute.particle_properties['Particle Identifier'].array
    for index in range(N):
        current_id = atoms_ids[index]
        for neigh in finder.find(index):
            neigh_index = neigh.index
            neigh_id = atoms_ids[neigh_index]
            min_results[current_id] = min(min_results[current_id], s[neigh_index])

    output = open("min_cg_results.dat",'w')
    for x in min_results:
        output.write("%f\n"%x)
    output.close()




# main process


def main():
    # Time start
    start_ticks = time.time()

    # Parse arguments
    parser = argparse.ArgumentParser(description=__doc__,
            epilog= """This is some addition description.
                    """,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-nt","--notime", help="Don't dispaly time usage.", action="store_true", default=False)
    parser.add_argument("-f","--format", help="Define the format of configuation.", default='lammps-dump')
    parser.add_argument("-nr","--nr", help="Define the number of r bins.", type=int, default=1000)
    parser.add_argument("-v","--value", help="Define the value file", default="lowest_triggering_strain_SS_0.dat")
    parser.add_argument("-mr","--mr", help="Define the maximum of r.", type=float, default=10.0)
    parser.add_argument("-ntheta","--ntheta", help="Define the number of theta bins.", type=int, default=50)
    parser.add_argument("-i","--infile", help="Define the configuration file.", default='dump.lammpstrj' )
    #parser.add_argument("-o","--outfile", help="Define the output file.", type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    # Your main process
    min_cg(args.value,filename=args.infile,cutoff=args.mr)
    
    # Time end
    end_tickes = time.time()
    # Output time usage
    if not args.notime:
        print("Time usage: %f s" % (end_tickes-start_ticks))
    return 0

if __name__ == "__main__":
    sys.exit(main())
