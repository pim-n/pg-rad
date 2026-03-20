import logging

from pg_rad.path.path import Path
from pg_rad.detector.detector import Detector
from pg_rad.objects.sources import PointSource


logger = logging.getLogger(__name__)


class Landscape:
    """
    A generic Landscape that can contain a Path and sources.
    """
    def __init__(
            self,
            name: str,
            path: Path,
            air_density: float,
            point_sources: list[PointSource],
            detector: Detector,
            size: tuple[int, int, int]
            ):
        """Initialize a landscape.

        Args:
            name (str): Name of the landscape.
            path (Path): The path of the detector.
            air_density (float): Air density in kg/m^3.
            point_sources (list[PointSource]): List of point sources.
            detector (Detector): The detector object.
            size (tuple[int, int, int]): Size of the world.
        """

        self.name = name
        self.path = path
        self.point_sources = point_sources
        self.size = size
        self.air_density = air_density
        self.detector = detector

        logger.debug(f"Landscape created: {self.name}")
