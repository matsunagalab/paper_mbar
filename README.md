# MBAR input files used in Matsunaga et al.

This repository contains input files for MBAR calculations used in "Use of multistate Bennett acceptance ratio method for free-energy calculations from enhanced sampling and free energy perturbation" by Matsunaga et al.

The files covers all the MBAR calculations except for the QM/MM case, the files of which are available from the authors upon reasonable request. 

All of the input files for mbar_analysis tool provided with the molecular dynamcis simulation software GENESIS.

## Descriptions on files

The files are organied as follows:

- [umbrella_alad/](https://github.com/matsunagalab/paper_mbar/tree/main/umbrella_alad) contains Umbrella sampling files

  - [umbrella_alad/5_mbar/mbar_analysis.inp](https://github.com/matsunagalab/paper_mbar/blob/main/umbrella_alad/5_mbar/mbar_analysis.inp) MBAR input

- [remd_alat/](https://github.com/matsunagalab/paper_mbar/tree/main/remd_alat) contains T-REMD files

  - [inp](https://github.com/matsunagalab/paper_mbar/blob/main/remd_alat/5_analysis/mbar/inp) MBAR input

- [fep_val2trp/](https://github.com/matsunagalab/paper_mbar/tree/main/fep_val2trp) contains FEP files

  - [mbar_analysis.inp](https://github.com/matsunagalab/paper_mbar/blob/main/fep_val2trp/5_analysis/mbar_analysis.inp) MBAR input

- [grest_alat/](https://github.com/matsunagalab/paper_mbar/tree/main/grest_alat) contains gREST files

  - [mbar_analysis.inp](https://github.com/matsunagalab/paper_mbar/blob/main/grest_alat/5_analysis/5-4_mbar/mbar/mbar.inp) MBAR input

## Acknowledgement

We acknowledgement the authors of GENESIS tutorials https://www.r-ccs.riken.jp/labs/cbrt/tutorials2022/ . Some of the input files are based on the tutorial files. 

## License

This repository is licensed under the under the terms of GNU General Public License v3.0. 
 
## Contact

Yasuhiro Matsunaga

ymatsunaga@mail.saitama-u.ac.jp

