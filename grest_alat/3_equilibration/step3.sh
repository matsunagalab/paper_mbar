#! /bin/bash -f
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -pe pe_parameter
#$ -q queue
#$ -N step3

export OMP_NUM_THREADS=3
bindir=/home/user/genesis/bin
nmpi=32
npernode=8
name=step3
mpicommand="mpiexec.hydra -f $TMP/machines -genv OMP_NUM_THREADS=$OMP_NUM_THREADS -genv I_MPI_FABRICS=shm:ofa  -ppn ${npernode} -np ${nmpi}"

$mpicommand ${bindir}/spdyn ${name}.inp >${name}.log 2>&1
~             
