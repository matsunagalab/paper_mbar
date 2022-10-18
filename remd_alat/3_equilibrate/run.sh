#!/bin/sh -f
#$ -S /bin/sh
#$ -V
#$ -N run
#$ -pe ompi 120
#$ -cwd
#$ -q q2.q
#$ -o run.log

rm *.{rst,dcd,rpath,log}
export OMP_NUM_THREADS=3
SPDYN=/home/yasu/gat/bin/spdyn
mpirun -machinefile $TMPDIR/machines -npernode 8 -np 40 $SPDYN run.inp >run.out

