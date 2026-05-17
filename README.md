[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-312/)
[![Tests](https://github.com/pim-n/pg-rad/actions/workflows/ci-tests.yml/badge.svg)](https://github.com/pim-n/pg-rad/actions/workflows/ci-tests.yml)
# PG-RAD - Primary Gamma RADiation landscape simulator

PG-RAD is a command-line software package for simulating localisation of orphan sources using mobile gamma spectrometry. PG-RAD provides a framework for construction road geometries, arbitrary distributions of point sources, modelling the detector response to primary gammas. PG-RAD provides a configurable framework for constructing detector trajectories, defining radioactive source distributions, modelling detector response, and generating synthetic acquisition data. User input is specified through YAML configuration files, which makes simulations reproducible and easily shared.

## Installation

PG-RAD is a Python 3 package and is only tested on x86_64 Linux systems. The following installation instructions were testing for a fresh virtual machine running Ubuntu 26.04 LTS.

## Conda installation (Tested and recommended)

1. Install git by `sudo apt update && sudo apt install git`
2. Install miniforge by following [these](https://conda-forge.org/download/) instructions.
3. Create a file called `environment.yml`, and paste the following in there:

```yaml
name: my-pgrad-env
channels:
  - conda-forge
dependencies:
  - python=3.12
  - pip:
    - git+ssh://git@github.com/pim-n/pg-rad.git@main
```
4. Run `conda env create -f environment.yml` to create the environment
5. Run `conda activate pg-rad-analysis`. You should now be in the conda environment `my-pgrad-env`.
6. To test if installation was succesful, run `pgrad --example --show`. If this runs without errors and produces visual output, PG-RAD is correctly installed.

## Manual installation

If you prefer another virtual environment, you still need git installed. Ensure the Python version of the environment is `>3.12.4` and `<3.13`. Then, with your virtual environment activated, run `pip install git+ssh://git@github.com/pim-n/pg-rad.git@main`. Run `pgrad --example --show` to check if the installation was successful.
