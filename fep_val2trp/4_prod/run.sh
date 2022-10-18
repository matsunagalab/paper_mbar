#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -pe ompi16 208
#$ -l h=!(squid23|squid24)
#$ -q all.q
#$ -N test

export OMP_NUM_THREADS=1

mpirun -machinefile $TMP/machines -npernode 16 -n 208 ./spdyn ./run.inp > output/run.out
