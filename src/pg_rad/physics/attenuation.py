from importlib.resources import files

from pandas import read_csv
from scipy.interpolate import interp1d

from pg_rad.configs.filepaths import ATTENUATION_TABLE


def get_mass_attenuation_coeff(
        *args
        ) -> float:
    csv = files('pg_rad.data').joinpath(ATTENUATION_TABLE)
    data = read_csv(csv)
    x = data["energy_mev"].to_numpy()
    y = data["mu"].to_numpy()
    f = interp1d(x, y)
    return f(*args)
