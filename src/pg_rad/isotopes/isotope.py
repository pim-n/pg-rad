from pg_rad.physics import get_mass_attenuation_coeff


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
