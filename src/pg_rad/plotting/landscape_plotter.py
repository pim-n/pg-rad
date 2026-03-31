import logging

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Circle

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
        ax.set_ylim(bottom=-.5*width, top=.5*width)

        ax.set_xlabel("X [m]")
        ax.set_ylabel("Y [m]")
        ax.set_title(f"Landscape (top-down, z = {self.z})")

    def _draw_path(self, ax, landscape: Landscape):
        if landscape.path.z <= self.z:
            ax.plot(
                landscape.path.x_list,
                landscape.path.y_list,
                linestyle='-',
                marker='|',
                markersize=3,
                linewidth=1
            )
            if len(landscape.path.x_list) >= 2:
                ax = self._draw_path_direction_arrow(ax, landscape.path)

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

    def _draw_path_direction_arrow(self, ax, path) -> Axes:
        inset_ax = ax.inset_axes([0.8, 0.1, 0.15, 0.15])

        x_start, y_start = path.x_list[0], path.y_list[0]
        x_end, y_end = path.x_list[1], path.y_list[1]

        dx = x_end - x_start
        dy = y_end - y_start

        if path.opposite_direction:
            dx = -dx
            dy = -dy

        length = 10
        dx_norm = dx / (dx**2 + dy**2)**0.5 * length
        dy_norm = dy / (dx**2 + dy**2)**0.5 * length

        inset_ax.arrow(
            0, 0,
            dx_norm, dy_norm,
            head_width=5, head_length=5,
            fc='red', ec='red',
            zorder=4, linewidth=1
        )

        inset_ax.set_xlim(-2*length, 2*length)
        inset_ax.set_ylim(-2*length, 2*length)
        inset_ax.set_title("Direction", fontsize=8)
        inset_ax.set_xticks([])
        inset_ax.set_yticks([])
        return ax
