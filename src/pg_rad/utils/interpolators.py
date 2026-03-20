from importlib.resources import files

import numpy as np
from pandas import read_csv
from scipy.interpolate import interp1d, CubicSpline

from pg_rad.configs.filepaths import ATTENUATION_TABLE


def get_mass_attenuation_coeff(*args) -> float:
    csv = files('pg_rad.data').joinpath(ATTENUATION_TABLE)
    data = read_csv(csv)
    x = data["energy_mev"].to_numpy()
    y = data["mu"].to_numpy()
    f = interp1d(x, y)
    return f(*args)


def get_field_efficiency(name: str, energy_keV: float) -> float:
    csv = files('pg_rad.data.field_efficiencies').joinpath(name+'.csv')
    data = read_csv(csv)
    data = data.groupby("energy_keV", as_index=False).mean()
    x = data["energy_keV"].to_numpy()
    y = data["field_efficiency_m2"].to_numpy()
    f = CubicSpline(x, y)
    return f(energy_keV)


def get_angular_efficiency(name: str, energy_keV: float, *angle: float):
    csv = files('pg_rad.data.angular_efficiencies').joinpath(name+'.csv')
    data = read_csv(csv)

    # check all energies at which angular eff. is available for this detector.
    # this is done within 1% tolerance
    energy_cols = [col for col in data.columns if col != "angle"]
    energies = np.array([float(col) for col in energy_cols])
    rel_diff = np.abs(energies - energy_keV) / energies
    match_idx = np.where(rel_diff <= 0.01)[0]

    if len(match_idx) == 0:
        raise NotImplementedError(
            f"No angular efficiency defined for {energy_keV} keV "
            f"in detector '{name}'. Available: {energies}"
        )

    best_idx = match_idx[np.argmin(rel_diff[match_idx])]
    selected_energy_col = energy_cols[best_idx]

    x = data["angle"].to_numpy()
    y = data[selected_energy_col].to_numpy()
    idx = np.argsort(x)
    x = x[idx]
    y = y[idx]
    f = interp1d(x, y)

    return f(angle)
