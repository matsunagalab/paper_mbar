#! /bin/bash -f
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -pe pe_parameter
#$ -q queue
#$ -N pmf
#$ -o pmf_o.log
#$ -e pmf_e.log

export OMP_NUM_THREADS=1
bindir=/opt/genesis/bin

${bindir}/pmf_analysis pmf.inp > pmf.log
