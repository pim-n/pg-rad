from abc import ABC


class BaseDetector(ABC):
    def __init__(
        self,
        name: str,
        efficiency: float
    ):
        self.name = name
        self.efficiency = efficiency

    def get_efficiency(self):
        pass


class IsotropicDetector(BaseDetector):
    def __init__(
        self,
        name: str,
        efficiency: float,
    ):
        super().__init__(name, efficiency)

    def get_efficiency(self, energy):
        return self.efficiency


class AngularDetector(BaseDetector):
    def __init__(
        self,
        name: str,
        efficiency: float
    ):
        super().__init__(name, efficiency)

    def get_efficiency(self, angle, energy):
        pass
