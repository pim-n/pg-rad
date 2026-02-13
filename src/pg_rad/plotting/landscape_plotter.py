import logging

from matplotlib import pyplot as plt
from matplotlib.patches import Circle

from pg_rad.landscape import Landscape


logger = logging.getLogger(__name__)


class LandscapeSlicePlotter:
    def plot(self, landscape: Landscape, z: int = 0):
        """Plot a top-down slice of the landscape at a height z.

        Args:
            landscape (Landscape): the landscape to plot
            z (int, optional): Height at which to plot slice. Defaults to 0.
        """        """

        """
        self.z = z
        fig, ax = plt.subplots()

        self._draw_base(ax, landscape)
        self._draw_path(ax, landscape)
        self._draw_point_sources(ax, landscape)

        ax.set_aspect("equal")
        plt.show()

    def _draw_base(self, ax, landscape):
        width, height = landscape.size[:2]
        ax.set_xlim(right=width)
        ax.set_ylim(top=height)
        ax.set_xlabel("X [m]")
        ax.set_ylabel("Y [m]")
        ax.set_title(f"Landscape (top-down, z = {self.z})")

    def _draw_path(self, ax, landscape):
        if landscape.path.z < self.z:
            ax.plot(landscape.path.x_list, landscape.path.y_list, 'bo-')
        else:
            logger.warning(
                "Path is above the slice height z."
                "It will not show on the plot."
                )

    def _draw_point_sources(self, ax, landscape):
        for s in landscape.point_sources:
            if s.z <= self.z:
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
            else:
                logger.warning(
                    f"Source {s.name} is above slice height z."
                    "It will not show on the plot."
                    )
