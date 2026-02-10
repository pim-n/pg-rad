import logging

from matplotlib import pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from numpy.typing import ArrayLike

from pg_rad.path import Path
from pg_rad.objects import PointSource
from pg_rad.physics.fluence import phi_single_source

logger = logging.getLogger(__name__)


class Landscape:
    """A generic Landscape that can contain a Path and sources.

    Args:
        air_density (float, optional): Air density, kg/m^3. Defaults to 1.243.
        size (int | tuple[int, int, int], optional): Size of the world.
        Defaults to 500.
        scale (str, optional): The scale of the size argument passed.
        Defaults to 'meters'.
    """
    def __init__(
            self,
            air_density: float = 1.243,
            size: int | tuple[int, int, int] = 500,
            scale: str = 'meters'
            ):
        if isinstance(size, int):
            self.world = np.zeros((size, size, size))
        elif isinstance(size, tuple) and len(size) == 3:
            self.world = np.zeros(size)
        else:
            raise TypeError("size must be integer or a tuple of 3 integers.")

        self.air_density = air_density
        self.scale = scale
        self.path: Path = None
        self.sources: list[PointSource] = []
        logger.debug("Landscape initialized.")

    def plot(self, z: float | int = 0):
        """Plot a slice of the world at a height `z`.

        Args:
            z (int, optional): Height of slice. Defaults to 0.

        Returns:
            fig, ax: Matplotlib figure objects.
        """
        x_lim, y_lim, _ = self.world.shape

        fig, ax = plt.subplots()
        ax.set_xlim(right=x_lim)
        ax.set_ylim(top=y_lim)
        ax.set_xlabel(f"X [{self.scale}]")
        ax.set_ylabel(f"Y [{self.scale}]")

        if self.path is not None:
            ax.plot(self.path.x_list, self.path.y_list, 'bo-')

        for s in self.sources:
            if np.isclose(s.z, z):
                dot = Circle(
                        (s.x, s.y),
                        radius=5,
                        color=s.color,
                        zorder=5
                )

                ax.text(
                    s.x + 0.06,
                    s.y + 0.06,
                    s.name,
                    color=s.color,
                    fontsize=10,
                    ha="left",
                    va="bottom",
                    zorder=6
                )

                ax.add_patch(dot)

        return fig, ax

    def add_sources(self, *sources: PointSource):
        """Add one or more point sources to the world.

        Args:
            *sources (pg_rad.sources.PointSource): One or more sources,
            passed as Source1, Source2, ...
        Raises:
            ValueError: If the source is outside the boundaries of the
            landscape.
        """
        if not any(
            (0 <= source.pos[0] <= self.world.shape[0] or
             0 <= source.pos[1] <= self.world.shape[1] or
             0 <= source.pos[2] <= self.world.shape[2])
            for source in sources
        ):
            raise ValueError("One or more sources are outside the landscape!")

        self.sources.extend(sources)

    def set_path(self, path: Path):
        """
        Set the path in the landscape.
        """
        if not isinstance(path, Path):
            raise TypeError("path must be of type Path.")
        self.path = path

    def calculate_fluence_at(self, pos: tuple):
        total_phi = 0.
        for source in self.sources:
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
        if self.path is None:
            raise ValueError("Path is not set!")


def create_landscape_from_path(path: Path, max_z: float | int = 50):
    """Generate a landscape from a path, using its dimensions to determine
    the size of the landscape.

    Args:
        path (Path): A Path object describing the trajectory.
        max_z (int, optional): Height of the world. Defaults to 50 meters.

    Returns:
        landscape (pg_rad.landscape.Landscape): A landscape with dimensions
        based on the provided Path.
    """
    max_x = np.ceil(max(path.x_list))
    max_y = np.ceil(max(path.y_list))

    landscape = Landscape(size=(max_x, max_y, max_z))
    landscape.path = path
    return landscape
