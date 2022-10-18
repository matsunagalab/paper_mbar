#!/bin/sh

charmm < charmm.inp
vmd -dispdev text -e solvate.tcl
