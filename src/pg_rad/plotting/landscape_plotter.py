import logging

from matplotlib import pyplot as plt
from matplotlib.patches import Circle

from pg_rad.landscape import Landscape

logger = logging.getLogger(__name__)


class LandscapeSlicePlotter:
    def plot(
        self,
        landscape: Landscape,
        z: int = 0,
        show: bool = True,
        save: bool = False
    ):
        """Plot a top-down slice of the landscape at a height z.

        Args:
            landscape (Landscape): the landscape to plot
            z (int, optional): Height at which to plot slice. Defaults to 0.
            show (bool, optional): Show the plot. Defaults to True.
            save (bool, optional): Save the plot. Defaults to False.
        """        """

        """
        self.z = z
        fig, ax = plt.subplots()

        self._draw_base(ax, landscape)
        self._draw_path(ax, landscape)
        self._draw_point_sources(ax, landscape)

        ax.set_aspect("equal")

        if save:
            name = landscape.name.lower().replace(' ', '_')
            plt.savefig(
                f"{name}_z{self.z}.png"
            )

        if show:
            plt.show()

    def _draw_base(self, ax, landscape):
        width, height = landscape.size[:2]
        ax.set_xlim(right=width)
        ax.set_ylim(top=height)
        ax.set_xlabel("X [m]")
        ax.set_ylabel("Y [m]")
        ax.set_title(f"Landscape (top-down, z = {self.z})")

    def _draw_path(self, ax, landscape):
        if landscape.path.z <= self.z:
            ax.plot(landscape.path.x_list, landscape.path.y_list, 'bo-')
        else:
            logger.warning(
                "Path is above the slice height z."
                "It will not show on the plot."
                )

    def _draw_point_sources(self, ax, landscape):
        for s in landscape.point_sources:
            x, y, z = s.pos
            if z <= self.z:
                dot = Circle(
                        (x, y),
                        radius=5,
                        color=s.color,
                        zorder=5
                )

                ax.text(
                    x + 0.06,
                    y + 0.06,
                    s.name+", z="+str(z),
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
