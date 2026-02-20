[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-312/)
[![Tests](https://github.com/pim-n/pg-rad/actions/workflows/ci-tests.yml/badge.svg)](https://github.com/pim-n/pg-rad/actions/workflows/ci-tests.yml)
# pg-rad
Primary Gamma RADiation landscape - Development

## Clone
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

## Dependencies / venv

With Python verion `>=3.12.4` and `<3.13`, create a virtual environment and install pg-rad.

```
python3 -m venv .venv
source .venv/bin/activate
```

With the virtual environment activated, run:

```
pip install -e .[dev]
```

## Running example landscape

The example landscape can be generated using the command-line interface. Still in the virtual environment, run

```
pgrad --test --loglevel DEBUG
```

## Tests

Tests can be run with `pytest` from the root directory of the repository. With the virtual environment activated, run:

```
pytest
```

## Local viewing of documentation

PG-RAD uses [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) for generating documentation. It can be locally viewed by (in the venv) running:
```
mkdocs serve
```

where you can add the `--livereload` flag to automatically update the documentation as you write to the Markdown files.
