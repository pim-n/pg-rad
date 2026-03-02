from abc import ABC
from dataclasses import dataclass


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
    pass


@dataclass
class ProceduralPathSpec(PathSpec):
    segments: list[str]
    angles: list[float]
    lengths: list[int | None]
    z: int | float
    alpha: float


@dataclass
class CSVPathSpec(PathSpec):
    file: str
    east_col_name: str
    north_col_name: str
    z: int | float


@dataclass
class SourceSpec(ABC):
    activity_MBq: float
    isotope: str
    name: str


@dataclass
class AbsolutePointSourceSpec(SourceSpec):
    x: float
    y: float
    z: float


@dataclass
class RelativePointSourceSpec(SourceSpec):
    along_path: float
    dist_from_path: float
    side: str
    z: float


@dataclass
class SimulationSpec:
    metadata: MetadataSpec
    runtime: RuntimeSpec
    options: SimulationOptionsSpec
    path: PathSpec
    point_sources: list[SourceSpec]
