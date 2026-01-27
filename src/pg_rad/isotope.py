class Isotope:
    def __init__(
            self,
            name: str,
            E: float,
            b: float
    ):
        """_Represents the essential information of an isotope._

        Args:
            name (str): Full name (e.g. Caesium-137).
            E (float): Energy of the primary gamma in keV.
            b (float): Branching ratio for the gamma at energy E.
        """        
        
        if E <= 0:
            raise ValueError("primary_gamma must be a positive energy (keV).")

        if not (0 <= b <= 1):
            raise ValueError("branching_ratio_pg must be a ratio (0 <= b <= 1)")

        self.name = name
        self.E = E
        self.b = b