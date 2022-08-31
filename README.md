# MBAR input files used in Matsunaga et al.

This repository contains input files for MBAR calculations, used in "Implementation of multistate Bennett acceptance ratio for versatile thermodynamic ensembles" by Matsunaga et al.

The files covers all the MBAR calculations exceptfor the QM/MM case, the files of which are available from the authors upon reasonable request. 

All of the input files for mbar_analysis tool provided with the molecular dynamcis simulation software GENESIS. You need to install GENESIS before using mbar_analysis. 

## Descriptions on files

The files are organied as follows:

- [umbrella_alad/](https://github.com/matsunagalab/paper_mbar/tree/main/umbrella_alad) contains Umbrella sampling files for alanine-dipeptide in vacuum

  - [inp](https://github.com/matsunagalab/paper_mbar/blob/main/umbrella_alad/5_mbar/mbar_analysis.inp) MBAR input file for Umbrella sampling data

- [remd_alat/](https://github.com/matsunagalab/mbar_paper/tree/main/remd_alat) contains T-REMD files for tri-alanine

  - [inp](https://github.com/matsunagalab/differentiable_BTR/blob/main/remd_alat/5_analysis/mbar/inp) MBAR input file for T-REMD data

## Acknowledgement

We acknowledgement the authors of GENESIS tutorials https://www.r-ccs.riken.jp/labs/cbrt/tutorials2022/ . Some of the input files are based on the tutorial files. 

## License

This repository is licensed under the under the terms of GNU General Public License v3.0. 
 
## Contact

Yasuhiro Matsunaga

ymatsunaga@mail.saitama-u.ac.jp

