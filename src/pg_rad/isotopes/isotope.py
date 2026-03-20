from importlib.resources import files

from pandas import read_csv

from pg_rad.configs.filepaths import ISOTOPE_TABLE
from pg_rad.exceptions.exceptions import InvalidIsotopeError
from pg_rad.utils.interpolators import get_mass_attenuation_coeff


class Isotope:
    """Represents the essential information of an isotope.

    Args:
        name (str): Full name (e.g. Caesium-137).
        E (float): Energy of the primary gamma in keV.
        b (float): Branching ratio for the gamma at energy E.
    """
    def __init__(
            self,
            name: str,
            E: float,
            b: float
    ):
        if E <= 0:
            raise ValueError("primary_gamma must be a positive energy (keV).")

        if not (0 <= b <= 1):
            raise ValueError("branching_ratio_pg must be a ratio b in [0,1]")

        self.name = name
        self.E = E
        self.b = b
        self.mu_mass_air = get_mass_attenuation_coeff(E / 1000)


def get_isotope(isotope: str, energy_gamma_keV: float) -> Isotope:
    """Lazy factory function to create isotope objects."""
    path = files('pg_rad.data').joinpath(ISOTOPE_TABLE)
    df = read_csv(path)

    isotope_df = df[df['isotope'] == isotope]

    if isotope_df.empty:
        raise InvalidIsotopeError(f"No data available for isotope {isotope}.")

    tol = 0.01 * energy_gamma_keV
    closest_energy = isotope_df[
        (isotope_df['gamma_energy_keV'] >= energy_gamma_keV - tol) &
        (isotope_df['gamma_energy_keV'] <= energy_gamma_keV + tol)
    ]

    if closest_energy.empty:
        available_gammas = ', '.join(
            str(x)+' keV' for x in isotope_df['gamma_energy_keV'].to_list()
        )
        raise InvalidIsotopeError(
            f"No gamma of {energy_gamma_keV}±{tol} keV "
            f"found for isotope {isotope}. "
            f"Available gammas are: {available_gammas}"
        )

    matched_row = closest_energy.iloc[0]
    return Isotope(
        name=isotope,
        E=matched_row['gamma_energy_keV'],
        b=matched_row['branching_ratio']
    )
