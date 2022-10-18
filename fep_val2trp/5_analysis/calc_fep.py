#!/usr/bin/env python

# usage: python3 ./calc_fep.py -n 26 -d ../4_prod/output -m exp -t 300.0
# usage: python3 ./calc_fep.py -n 26 -d ../4_prod/output -m bar -t 300.0

import sys, os
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--nlambda', dest='nlambda', required=True, help='number of lambda windows')
parser.add_argument('-d', '--data_directory', dest='data_directory', required=True, help='directory where fepout files are stored')
parser.add_argument('-m', '--method', dest='method', choices=['bar', 'exp'], required=True, help='method for free energy estimation')
parser.add_argument('-v', '--verbose', action='store_const', const=True, default=False, help='print out logs of mbar_analysis')
parser.add_argument('-t', '--temperature', dest='temperature', default='300', help='temperature')
args = parser.parse_args()

data_directory = args.data_directory
nlambda = int(args.nlambda)
verbose = args.verbose
temperature = float(args.temperature)
kB = 1.3806488*6.02214129/1000.0
beta = 1./(kB*temperature)
cal2j = 4.1841

# Bennett acceptance ratio
if args.method == 'bar':

    # Initialize free energy and error
    ddG = np.zeros(nlambda-1, float)
    se  = np.zeros(nlambda-1, float)

    f = open("temp.inp", "w")
    f.write("[INPUT]\n")
    f.write("cvfile    = ./run.fepout{}\n")
    f.write("[OUTPUT]\n")
    f.write("fenefile   = fene.dat\n")
    f.write("[MBAR]\n")
    f.write("nreplica       = 2\n")
    f.write("dimension      = 1\n")
    f.write("nblocks        = 3\n")
    f.write("input_type     = FEP\n")
    f.write("temperature    = 300.0\n")
    f.write("target_temperature    = 300.0\n")
    f.write("tolerance      = 1.0E-08\n")
    f.write("output_unit   = kcal/mol\n")
    f.close()

    for i in range(1, nlambda):
        # Merge results of foward calculations.
        f = open("%s/run.fepout%d" % (data_directory, i))
        lines = f.readlines()
        f.close()
        n = 0
        f_fwd = open("run.fepout1", "w")
        for line in lines:
            if not line.startswith("#"):
                a = line.split()
                f_fwd.write("%s %s %s %s\n" % (a[0], a[1], 0.0, a[3]))
                n += 1
        f_fwd.close()

        # Merge results of backward calculations.
        f = open("%s/run.fepout%d" % (data_directory, i+1))
        lines = f.readlines()
        f.close()
        n = 0
        f_bwd = open("run.fepout2", "w")
        for line in lines:
            if not line.startswith("#"):
                a = line.split()
                f_bwd.write("%s %s %s %s\n" % (a[0], a[1], a[2], 0.0))
                n += 1
        f_bwd.close()

        # Call MBAR analysis tool
        if verbose:
            os.system("./mbar_analysis ./temp.inp")
        else:
            os.system("./mbar_analysis ./temp.inp > /dev/null")
        f = open("fene.dat")
        line = f.readlines()[1]
        f.close
        os.system("rm run.fepout1 run.fepout2 fene.dat")

        # Calculate free energy change and error
        a = line.split()
        ndata = len(a)
        ddG_temp = np.zeros(ndata, float)
        for j in range(ndata):
            ddG_temp[j] = float(a[j])
        ddG[i-1] = ddG_temp.mean()
        #se[i-1]  = ddG_temp.std(ddof=1)/np.sqrt(ndata)
        se[i-1]  = ddG_temp.std(ddof=1)

    os.system("rm temp.inp")

    # Output results
    print("#    window          ddG    ddG_error           dG     dG_error")
    dG = 0.0
    se_total = 0.0
    for i in range(nlambda-1):
        dG += ddG[i]
        se_total = np.sqrt(se_total*se_total + se[i]*se[i])
        print("%3d <-> %3d %12.4f %12.4f %12.4f %12.4f" % (i+1, i+2, ddG[i], se[i], dG, se_total))


# Zwanzig EXP
elif args.method == 'exp':
    # Initialize
    exp_f = np.zeros(nlambda-1, float)
    exp_r = np.zeros(nlambda-1, float)
    n_f = np.zeros(nlambda-1, int)
    n_r = np.zeros(nlambda-1, int)

    for i in range(1, nlambda):
        # Merge results of foward calculations.
        for line in open("%s/run.fepout%d" % (data_directory, i)):
            if not line.startswith("#"):
                a = line.split()
                exp_f[i-1] += np.exp(-beta*cal2j*float(a[3]))
                n_f[i-1] += 1

        # Merge results of backward calculations.
        for line in open("%s/run.fepout%d" % (data_directory, i+1)):
            if not line.startswith("#"):
                a = line.split()
                exp_r[i-1] += np.exp(-beta*cal2j*float(a[2]))
                n_r[i-1] += 1

    # Output results
    print("#   window          ddG           dG")
    dG_f = 0.0
    for i in range(nlambda-1):
        ddG_f = -np.log(exp_f[i]/n_f[i])/(beta*cal2j)
        dG_f += ddG_f
        print("%3d -> %3d %12.4f %12.4f" % (i+1, i+2, ddG_f, dG_f))

    dG_r = dG_f
    for i in range(nlambda-2,-1,-1):
        ddG_r = -np.log(exp_r[i]/n_r[i])/(beta*cal2j)
        dG_r += ddG_r
        print("%3d -> %3d %12.4f %12.4f" % (i+2, i+1, ddG_r, dG_r))
