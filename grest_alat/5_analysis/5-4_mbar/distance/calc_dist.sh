#! /bin/bash -f
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -pe pe_parameter
#$ -q queue
#$ -N dist
#$ -o dist_o.log
#$ -e dist_e.log

export OMP_NUM_THREADS=1
bindir=/opt/genesis/bin

${bindir}/trj_analysis inp1 > log1
${bindir}/trj_analysis inp2 > log2
${bindir}/trj_analysis inp3 > log3
${bindir}/trj_analysis inp4 > log4
