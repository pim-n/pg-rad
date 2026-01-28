# Welcome!

Primary Gamma RADiation Landscapes (PG-RAD) is a Python package for research in source localization. It can simulate mobile gamma spectrometry data acquired from vehicle-borne detectors along a predefined path (e.g. a road).

## Requirements

PG-RAD requires Python `3.12`. The guides below assume a unix-like system.

## Installation (CLI)

<!--pipx seems like a possible option to install python package in a contained environment on unix-->

Lorem ipsum

## Installation (Python module)

If you are interested in using PG-RAD in another Python project, create a virtual environment first:

```
python3 -m venv .venv
```

Then install PG-RAD in it:

```
source .venv/bin/activate
(.venv) pip install git+https://github.com/pim-n/pg-rad
```

See how to get started with PG-RAD with your own Python code [here](pg-rad-in-python).

## For developers
```
git clone https://github.com/pim-n/pg-rad
cd pg-rad
git checkout dev
```

or

```
git@github.com:pim-n/pg-rad.git
cd pg-rad
git checkout dev
```