from typing import Dict, Type

from pg_rad.physics.attenuation import get_mass_attenuation_coeff


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


class CS137(Isotope):
    def __init__(self):
        super().__init__(
            name="Cs-137",
            E=661.66,
            b=0.851
        )


preset_isotopes: Dict[str, Type[Isotope]] = {
    "CS137": CS137
}


def get_isotope(isotope_str: str) -> Isotope:
    """Lazy factory function to create isotope objects."""
    if isotope_str not in preset_isotopes:
        raise ValueError(f"Unknown isotope: {isotope_str}")
    return preset_isotopes[isotope_str]()
