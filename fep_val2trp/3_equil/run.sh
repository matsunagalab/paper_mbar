#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -pe ompi16 64
#$ -l h=!(squid23|squid24)
#$ -q que2.q
#$ -N test

export OMP_NUM_THREADS=8

mpirun -machinefile $TMP/machines -npernode 2 -n 8 ./spdyn ./run.inp > output/run.out
