from .isotope import Isotope


class CS137(Isotope):
    def __init__(self):
        super.__init__(
            name="Cs-137",
            E=661.66,
            b=0.851
        )
