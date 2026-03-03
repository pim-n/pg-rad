from abc import ABC


class BaseDetector(ABC):
    def __init__(
        self,
        name: str,
        eff: float
    ):
        self.name = name
        self.eff = eff

    def get_efficiency(self):
        pass


class IsotropicDetector(BaseDetector):
    def __init__(
        self,
        name: str,
        eff: float | None = None
    ):
        super().__init__(name, eff)

    def get_efficiency(self, energy):
        return self.eff


class AngularDetector(BaseDetector):
    def __init__(
        self,
        name: str,
        eff: float | None = None
    ):
        super().__init__(name, eff)

    def get_efficiency(self, angle, energy):
        pass
