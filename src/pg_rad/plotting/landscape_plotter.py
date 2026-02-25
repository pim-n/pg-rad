import logging

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Circle

from numpy import median

from pg_rad.landscape.landscape import Landscape

logger = logging.getLogger(__name__)


class LandscapeSlicePlotter:
    def plot(
        self,
        landscape: Landscape,
        z: int = 0,
        show: bool = True,
        save: bool = False,
        ax: Axes | None = None
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

        if not ax:
            fig, ax = plt.subplots()

        self._draw_base(ax, landscape)
        self._draw_path(ax, landscape)
        self._draw_point_sources(ax, landscape)

        ax.set_aspect("equal")

        if save and not ax:
            landscape_name = landscape.name.lower().replace(' ', '_')
            filename = f"{landscape_name}_z{self.z}.png"
            plt.savefig(filename)
            logger.info("Plot saved to file: "+filename)

        if show and not ax:
            plt.show()

        return ax

    def _draw_base(self, ax, landscape: Landscape):
        width, height = landscape.size[:2]

        ax.set_xlim(right=max(width, .5*height))

        # if the road is very flat, we center it vertically (looks better)
        if median(landscape.path.y_list) == 0:
            h = max(height, .5*width)
            ax.set_ylim(bottom=-h//2,
                        top=h//2)
        else:
            ax.set_ylim(top=max(height, .5*width))

        ax.set_xlabel("X [m]")
        ax.set_ylabel("Y [m]")
        ax.set_title(f"Landscape (top-down, z = {self.z})")

    def _draw_path(self, ax, landscape):
        if landscape.path.z <= self.z:
            ax.plot(
                landscape.path.x_list,
                landscape.path.y_list,
                linestyle='-',
                marker='|',
                markersize=3,
                linewidth=1
            )
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
