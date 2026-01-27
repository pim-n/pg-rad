class Isotope:
    def __init__(
            self,
            name: str,
            E: float,
            b: float
    ):
        """_Represents the essential information of an isotope._

        Args:
            name (str): _Full name (e.g. Caesium-137)._
            E (float): _Energy of the primary gamma in keV._
            b (float): _Branching ratio for the gamma at energy E._
        """        
        
        if E <= 0:
            raise ValueError("primary_gamma must be a positive energy (keV).")

        if not (0 <= b <= 1):
            raise ValueError("branching_ratio_pg must be a ratio (0 <= b <= 1)")

        self.name = name
        self.E = E
        self.b = b