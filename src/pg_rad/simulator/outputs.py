from typing import List, Tuple

from dataclasses import dataclass


@dataclass
class CountRateOutput:
    arc_length: List[float]
    count_rate: List[float]


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
