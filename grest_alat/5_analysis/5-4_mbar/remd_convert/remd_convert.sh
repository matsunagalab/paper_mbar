#! /bin/bash -f
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -pe pe_parameter
#$ -q queue
#$ -N remd_convert
#$ -o remd_convert_o.log
#$ -e remd_convert_e.log

export OMP_NUM_THREADS=1
bindir=/home/user/genesis/bin

${bindir}/remd_convert remd_convert.inp > remd_convert.log
