from matplotlib import pyplot as plt
from matplotlib.patches import Circle
import numpy as np

from pg_rad.path import Path
from pg_rad.objects import Source

class Landscape:
    def __init__(self, size: int | tuple[int, int, int] = 500, unit = 'meters'):
        if isinstance(size, int):
            self.world = np.zeros((size, size, size))
        elif isinstance(size, tuple) and len(size) == 3:
            self.world = np.zeros(size)
        else:
            raise TypeError("size must be an integer or a tuple of 3 integers.")

        self.unit = unit

        self.path: Path = None
        self.sources: list[Source] = []
    
    def plot(self, z = 0):
        """_Plot a slice of the world at a height z._

        Args:
            z (int, optional): Height of slice. Defaults to 0.

        Returns:
            fig, ax: Matplotlib figure objects.
        """        
        x_lim, y_lim, _ = self.world.shape

        fig, ax = plt.subplots()
        ax.set_xlim(right=x_lim)
        ax.set_ylim(top=y_lim)
        ax.set_xlabel(f"X [{self.unit}]")
        ax.set_ylabel(f"Y [{self.unit}]")

        if not self.path == None:
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

    def add_sources(self, *sources: Source):
        """Add one or more point sources to the world."""

        max_x, max_y, max_z = self.world.shape[:3]

        if any(
            not (0 <= source.x < max_x and
                 0 <= source.y < max_y and
                 0 <= source.z < max_z)
            for source in sources
        ):
            raise ValueError("One or more sources are outside the world boundaries.")

        self.sources.extend(sources)

    def set_path(self, path: Path):
        self.path = path
    
def create_landscape_from_path(path: Path, max_z = 500):
    """_Generate a Landscape from a path, using its dimensions to determine
    the size of the Landscape._

    Args:
        path (Path): _A Path object describing the trajectory._
        max_z (int, optional): _Height of the world_. Defaults to 500 meters.

    Returns:
        _type_: _A Landscape with dimensions based on the provided Path._
    """    
    max_x = np.ceil(max(path.x_list))
    max_y = np.ceil(max(path.y_list))

    landscape = Landscape(
        size = (max_x, max_y, max_z)
        )
    
    landscape.path = path
    return landscape