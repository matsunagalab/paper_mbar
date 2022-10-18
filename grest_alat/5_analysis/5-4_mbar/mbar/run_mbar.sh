#! /bin/bash -f
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -pe pe_parameter
#$ -q queue
#$ -N mbar
#$ -o mbar_o.log
#$ -e mbar_e.log

export OMP_NUM_THREADS=1
bindir=/home/user/genesis/bin

${bindir}/mbar_analysis mbar.inp > mbar.log
