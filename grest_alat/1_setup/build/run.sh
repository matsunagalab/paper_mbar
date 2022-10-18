#!/bin/sh
exedir=/home/suyongre/data/genesis_tutorial/apps/charmm/c40b1/exec/em64t_M
${exedir}/charmm < charmm.inp
vmd -dispdev text -e solvate.tcl
