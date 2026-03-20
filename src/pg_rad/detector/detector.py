from importlib.resources import files

from pandas import read_csv

from pg_rad.utils.interpolators import (
    get_field_efficiency, get_angular_efficiency
)


class Detector:
    def __init__(
        self,
        name: str,
        type: str,
        is_isotropic: bool
    ):
        self.name = name
        self.type = type
        self.is_isotropic = is_isotropic

    def get_efficiency(self, energy_keV, angle=None):
        f_eff = get_field_efficiency(self.name, energy_keV)

        if self.is_isotropic or angle is None:
            return f_eff
        else:
            f_eff = get_field_efficiency(self.name, energy_keV)
            a_eff = get_angular_efficiency(self.name, energy_keV, *angle)
            return f_eff * a_eff


def load_detector(name) -> Detector:
    csv = files('pg_rad.data').joinpath('detectors.csv')
    data = read_csv(csv)
    dets = data['name'].values
    if name in dets:
        row = data[data['name'] == name].iloc[0]
        return Detector(row['name'], row['type'], row['is_isotropic'])
    else:
        raise NotImplementedError(
            f"Detector with name '{name}' not in detector library. Available:"
            f"{', '.join(dets)}"
        )
