import logging
from typing import Self

from pg_rad.dataloader import load_data
from pg_rad.exceptions import OutOfBoundsError
from pg_rad.objects import PointSource
from pg_rad.path import Path, path_from_RT90
from pg_rad.physics.fluence import phi_single_source

logger = logging.getLogger(__name__)


class Landscape:
    """
    A generic Landscape that can contain a Path and sources.
    """
    def __init__(
            self,
            name: str,
            path: Path,
            point_sources: list[PointSource] = [],
            size: tuple[int, int, int] = [500, 500, 50],
            air_density: float = 1.243
            ):
        """Initialize a landscape.

        Args:
            path (Path): A Path object.
            point_sources (list[PointSource], optional): List of point sources.
            air_density (float, optional): Air density in kg/m^3.
                Defaults to 1.243.
            size (tuple[int, int, int], optional): (x,y,z) dimensions of world
                in meters. Defaults to [500, 500, 50].

        Raises:
            TypeError: _description_
        """

        self.name = name
        self.path = path
        self.point_sources = point_sources
        self.size = size
        self.air_density = air_density

        logger.debug(f"Landscape created: {self.name}")

    def calculate_fluence_at(self, pos: tuple):
        total_phi = 0.
        for source in self.point_sources:
            r = source.distance_to(pos)
            phi_source = phi_single_source(
                r=r,
                activity=source.activity,
                branching_ratio=source.isotope.b,
                mu_mass_air=source.isotope.mu_mass_air,
                air_density=self.air_density
            )
            total_phi += phi_source
        return total_phi

    def calculate_fluence_along_path(self):
        pass


class LandscapeBuilder:
    def __init__(self, name: str = "Unnamed landscape"):
        self.name = name
        self._path = None
        self._point_sources = []
        self._size = None
        self._air_density = None

        logger.debug(f"LandscapeBuilder initialized: {self.name}")

    def set_air_density(self, air_density) -> Self:
        """Set the air density of the world."""
        self._air_density = air_density
        return self

    def set_landscape_size(self, size: tuple[int, int, int]) -> Self:
        """Set the size of the landscape in meters (x,y,z)."""
        if self._path and any(p > s for p, s in zip(self._path.size, size)):
            raise OutOfBoundsError(
                "Cannot set landscape size smaller than the path."
            )

        self._size = size
        logger.debug("Size of the landscape has been updated.")

        return self

    def set_path_from_experimental_data(
        self,
        filename: str,
        z: int,
        east_col: str = "East",
        north_col: str = "North"
    ) -> Self:
        df = load_data(filename)
        self._path = path_from_RT90(
            df=df,
            east_col=east_col,
            north_col=north_col,
            z=z
        )

        # The size of the landscape will be updated if
        # 1) _size is not set, or
        # 2) _size is too small to contain the path.
        needs_resize = (
            not self._size
            or any(p > s for p, s in zip(self._path.size, self._size))
        )

        if needs_resize:
            if not self._size:
                logger.debug("Because no Landscape size was set, "
                             "it will now set to path dimensions.")
            else:
                logger.warning(
                    "Path exceeds current landscape size. "
                    "Landscape size will be expanded to accommodate path."
                )

            self.set_landscape_size(self._path.size)

        return self

    def set_point_sources(self, *sources):
        """Add one or more point sources to the world.

        Args:
            *sources (pg_rad.sources.PointSource): One or more sources,
            passed as Source1, Source2, ...
        Raises:
            OutOfBoundsError: If any source is outside the boundaries of the
            landscape.
        """

        if any(
            any(p < 0 or p >= s for p, s in zip(source.pos, self._size))
            for source in sources
        ):
            raise OutOfBoundsError(
                "One or more sources attempted to "
                "be placed outside the landscape."
                )

        self._point_sources = sources

    def build(self):
        landscape = Landscape(
            name=self.name,
            path=self._path,
            point_sources=self._point_sources,
            size=self._size,
            air_density=self._air_density
        )

        logger.info(f"Landscape built successfully: {landscape.name}")
        return landscape
