import logging
from typing import Literal, Self

import numpy as np

from .landscape import Landscape
from pg_rad.dataloader.dataloader import load_data
from pg_rad.objects.sources import PointSource
from pg_rad.exceptions.exceptions import OutOfBoundsError
from pg_rad.utils.projection import rel_to_abs_source_position
from pg_rad.inputparser.specs import (
    SimulationSpec,
    CSVPathSpec,
    AbsolutePointSourceSpec,
    RelativePointSourceSpec,
    DetectorSpec
)
from pg_rad.detector.detector import load_detector
from pg_rad.path.path import Path, path_from_RT90

from road_gen.generators.segmented_road_generator import SegmentedRoadGenerator


logger = logging.getLogger(__name__)


class LandscapeBuilder:
    def __init__(self, name: str = "Unnamed landscape"):
        self.name = name
        self._path = None
        self._point_sources = []
        self._size = None
        self._air_density = 1.243
        self._detector = None

        logger.debug(f"LandscapeBuilder initialized: {self.name}")

    def set_air_density(self, air_density: float | None) -> Self:
        """Set the air density of the world."""
        if air_density and isinstance(air_density, float):
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

    def get_path(self):
        return self._path

    def set_path_from_segments(
        self,
        sim_spec: SimulationSpec
    ):
        path = sim_spec.path
        segments = path.segments
        lengths = path.lengths
        angles = path.angles
        alpha = path.alpha
        z = path.z

        sg = SegmentedRoadGenerator(
            ds=sim_spec.runtime.speed * sim_spec.runtime.acquisition_time,
            velocity=sim_spec.runtime.speed,
            seed=sim_spec.options.seed
        )

        x, y = sg.generate(
            segments=segments,
            lengths=lengths,
            angles=angles,
            alpha=alpha
        )

        self._path = Path(
            list(zip(x, y)),
            z=z,
            opposite_direction=path.opposite_direction
        )
        self._fit_landscape_to_path()
        return self

    def set_path_from_experimental_data(
        self,
        spec: CSVPathSpec
    ) -> Self:
        df = load_data(spec.file)
        self._path = path_from_RT90(
            df=df,
            east_col=spec.east_col_name,
            north_col=spec.north_col_name,
            z=spec.z,
            opposite_direction=spec.opposite_direction
        )

        self._fit_landscape_to_path()

        return self

    def set_point_sources(
        self,
        *sources: AbsolutePointSourceSpec | RelativePointSourceSpec
    ):
        """Add one or more point sources to the world.

        Args:
            *sources (AbsolutePointSourceSpec | RelativePointSourceSpec):
                One or more sources, passed as SourceSpecs tuple
        Raises:
            OutOfBoundsError: If any source is outside the boundaries of the
            landscape.
        """

        for s in sources:
            if isinstance(s, AbsolutePointSourceSpec):
                pos = (s.x, s.y, s.z)
            elif isinstance(s, RelativePointSourceSpec):
                path = self.get_path()

                if s.alignment:
                    along_path = self._align_relative_source(
                        s.along_path,
                        path,
                        s.alignment
                    )
                    logger.info(
                        f"Because source {s.name} was set to align with path "
                        f"({s.alignment} alignment), it was moved to be at "
                        f"{along_path} m along the path from {s.along_path} m."
                    )
                else:
                    along_path = s.along_path
                pos = rel_to_abs_source_position(
                    x_list=path.x_list,
                    y_list=path.y_list,
                    path_z=path.z,
                    along_path=along_path,
                    side=s.side,
                    dist_from_path=s.dist_from_path)

            # we dont support -x values, but negative y values are possible as
            # the path is centered in the y direction.
            print(pos)
            if not (
                (0 < pos[0] < self._size[0]) and
                (-0.5 * self._size[1] < pos[1] < 0.5 * self._size[1])
            ):
                raise OutOfBoundsError(
                    "One or more sources attempted to "
                    "be placed outside the landscape."
                    )

            self._point_sources.append(PointSource(
                activity_MBq=s.activity_MBq,
                isotope=s.isotope,
                position=pos,
                name=s.name
            ))

    def set_detector(self, spec: DetectorSpec) -> Self:
        self._detector = load_detector(spec.name)
        return self

    def _fit_landscape_to_path(self) -> None:
        """The size of the landscape will be updated if
        1) _size is not set, or
        2) _size is too small to contain the path."""

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

            max_size = max(self._path.size)
            self.set_landscape_size((max_size, max_size))

    def _align_relative_source(
        self,
        along_path: float,
        path: "Path",
        mode: Literal["best", "worst"],
    ) -> tuple[float, float, float]:
        """Given the arc length at which the point source is placed,
            align the source relative to the waypoints of the path. Here,
            'best' means the point source is moved such that it is
            perpendicular to the midpoint between two acuisition points.
            'worst' means the point source is moved such that it is
            perpendicular to the nearest acquisition point.

            The distance to the path is not affected by this algorithm.

            For more details on alignment, see
            Fig. 4 and page 24 in Bukartas (2021).

        Args:
            along_path (float): Current arc length position of the source.
            path (Path): The path to align to.
            mode (Literal["best", "worst"]): Alignment mode.

        Returns:
            along_new (float): The updated arc length position.
        """
        ds = np.hypot(
            path.x_list[1] - path.x_list[0],
            path.y_list[1] - path.y_list[0],
        )

        if mode == "worst":
            along_new = round(along_path / ds) * ds

        elif mode == "best":
            along_new = (round(along_path / ds - 0.5) + 0.5) * ds

        else:
            raise ValueError(f"Unknown alignment mode: {mode}")

        return along_new

    def build(self):
        landscape = Landscape(
            name=self.name,
            path=self._path,
            point_sources=self._point_sources,
            detector=self._detector,
            size=self._size,
            air_density=self._air_density
        )

        logger.info(f"Landscape built successfully: {landscape.name}")
        return landscape
