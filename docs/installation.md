## Requirements

PG-RAD requires Python `>=3.12.4` and `<3.13`. It has been tested on `3.12.9`. The guides below assume a unix-like system. You can check the Python version you have installed as follows:

```
python --version
```

If you don't have the right version installed there are various ways to get a compatible version, such as [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation).

## Installation (CLI)

<!--pipx seems like a possible option to install python package in a contained environment on unix-->

Lorem ipsum

## Installation (Python module)

If you are interested in using PG-RAD in another Python project, create a virtual environment first:

```
python -m venv .venv
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