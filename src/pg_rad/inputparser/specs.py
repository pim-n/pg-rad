from abc import ABC
from dataclasses import dataclass
from typing import Literal


@dataclass
class MetadataSpec:
    name: str


@dataclass
class RuntimeSpec:
    speed: float
    acquisition_time: float


@dataclass
class SimulationOptionsSpec:
    air_density: float
    seed: int | None = None


@dataclass
class PathSpec(ABC):
    z: int | float
    opposite_direction: bool


@dataclass
class ProceduralPathSpec(PathSpec):
    segments: list[str]
    angles: list[float]
    lengths: list[int | None]
    alpha: float


@dataclass
class CSVPathSpec(PathSpec):
    file: str
    east_col_name: str
    north_col_name: str


@dataclass
class PointSourceSpec(ABC):
    activity_MBq: float
    isotope: str
    name: str


@dataclass
class AbsolutePointSourceSpec(PointSourceSpec):
    x: float
    y: float
    z: float


@dataclass
class RelativePointSourceSpec(PointSourceSpec):
    along_path: float
    dist_from_path: float
    side: str
    z: float
    alignment: Literal["best", "worst"] | None


@dataclass
class DetectorSpec:
    name: str


@dataclass
class SimulationSpec:
    metadata: MetadataSpec
    runtime: RuntimeSpec
    options: SimulationOptionsSpec
    path: PathSpec
    point_sources: list[PointSourceSpec]
    detector: DetectorSpec
