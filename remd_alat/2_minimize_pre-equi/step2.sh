#! /bin/bash -f
#
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -pe ompi16 16
#$ -q nogpu.q
#$ -N minim_pre-equi

export OMP_NUM_THREADS=2
bindir=/home/user/genesis/bin

mpirun -machinefile ${TMP}/machines -np 8 -npernode 8  ${bindir}/spdyn step2.1.inp > step2.1.log
mpirun -machinefile ${TMP}/machines -np 8 -npernode 8  ${bindir}/spdyn step2.2.inp > step2.2.log
mpirun -machinefile ${TMP}/machines -np 8 -npernode 8  ${bindir}/spdyn step2.3.inp > step2.3.log
mpirun -machinefile ${TMP}/machines -np 8 -npernode 8  ${bindir}/spdyn step2.4.inp > step2.4.log
