#! /bin/bash -f
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -pe pe_parameter
#$ -q queue
#$ -N remd_conv
#$ -o remd_conv_o.log
#$ -e remd_conv_e.log

export OMP_NUM_THREADS=1

name=remd_conv
#for ((num=1; num<=3; num++)); do
for ((num=1; num<=1; num++)); do
     remd_convert ${name}.${num}.inp >${name}.${num}.log 2>&1
done
