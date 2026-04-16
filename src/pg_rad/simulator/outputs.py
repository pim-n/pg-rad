from typing import List, Tuple

from dataclasses import dataclass


@dataclass
class CountRateOutput:
    x: List[float]
    y: List[float]
    distance: List[float]
    sub_points: List[float]
    cps: List[float]
    integrated_counts: List[float]
    mean_bkg_cps: List[float]


@dataclass
class SourceOutput:
    name: str
    isotope: str
    primary_gamma: float
    activity: float
    position: Tuple[float, float, float]
    dist_from_path: float


@dataclass
class DetectorOutput:
    name: str
    type: str
    is_isotropic: bool
    field_eff: float


@dataclass
class SimulationOutput:
    name: str
    size: tuple
    detector: DetectorOutput
    count_rate: CountRateOutput
    sources: List[SourceOutput]
