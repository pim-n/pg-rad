from typing import List, Tuple

from dataclasses import dataclass


@dataclass
class CountRateOutput:
    acquisition_points: List[float]
    sub_points: List[float]
    cps: List[float]
    integrated_counts: List[float]


@dataclass
class SourceOutput:
    name: str
    isotope: str
    primary_gamma: float
    activity: float
    position: Tuple[float, float, float]
    dist_from_path: float


@dataclass
class SimulationOutput:
    name: str
    count_rate: CountRateOutput
    sources: List[SourceOutput]
