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

With Python verion `>=3.12.4`, create a virtual environment and install pg-rad.

```
python3 -m venv .venv
source .venv/bin/activate
(venv) pip install -e .[dev]
```

## Tests

Tests can be run with `pytest` from the root directory of the repository.

```
(venv) pytest
```