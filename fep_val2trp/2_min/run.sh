#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -pe ompi16 32
#$ -l h=!(squid23|squid24)
#$ -q que2.q
#$ -N test

export OMP_NUM_THREADS=4

mpirun -machinefile $TMP/machines -npernode 4 -n 8 ./spdyn ./run.inp > output/run.out
