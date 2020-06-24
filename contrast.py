#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Calculate the contrast between two array.
"""
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# Python template written by Bin Xu (xubinrun@gmail.com)
# Licensed under GPL License


import argparse
import sys
import numpy as np
import time

def contrast(a,b):
    """
    Calculate the contrast between array a and b.
    
    Parameters:

    a: float array
    
    b: float array

    Return: a contrast float array

    contrast = |a-b|/((a+b)/2)

    """
    aa = np.array(a,dtype=np.double)
    bb = np.array(b,dtype=np.double)
    return np.fabs(aa-bb)/(aa+bb)*2.0


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
    #parser.add_argument("-k","--key", help="Define the key column.", type=int, default=1, metavar='col_num', nargs='+')
    parser.add_argument("infile", help="Define the input file.", nargs=2)
    parser.add_argument("-o","--outfile", help="Define the output file.", type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    # Your main process
    with open(args.infile[0]) as indata:
        a = [np.double(x) for x in indata if x[0] != '#']
    
    with open(args.infile[1]) as indata:
        b = [np.double(x) for x in indata if x[0] != '#']

    results = contrast(a,b)

    out = args.outfile
    for ir in results:
        out.write("%16g\n" % ir)
    out.close()


    # Time end
    end_tickes = time.time()
    # Output time usage
    if not args.notime:
        print("Time usage: %f s" % (end_tickes-start_ticks))
    return 0

if __name__ == "__main__":
    sys.exit(main())
