#! /bin/bash -f
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -pe pe_parameter
#$ -q queue
#$ -N step4

export OMP_NUM_THREADS=3
nmpi=32
npernode=8
name=step4
bindir=/home/user/genesis/bin

mpicommand="mpiexec.hydra -f $TMP/machines -genv OMP_NUM_THREADS=$OMP_NUM_THREADS -genv I_MPI_FABRICS=shm:ofa  -ppn ${npernode} -np ${nmpi}"
#for ((num=1; num<=3; num++)); do
for ((num=1; num<=1; num++)); do
     $mpicommand ${bindir}/spdyn ${name}.${num}.inp >${name}.${num}.log 2>&1
done

~             
