from collections.abc import Sequence
import logging
import math

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


class PathSegment:
    def __init__(self, a: tuple[float, float], b: tuple[float, float]):
        """A straight Segment of a Path, from (x_a, y_a) to (x_b, y_b).

        Args:
            a (tuple[float, float]): The starting point (x_a, y_a).
            b (tuple[float, float]): The final point (x_b, y_b).
        """
        self.a = a
        self.b = b

    def get_length(self) -> float:
        return math.dist(self.a, self.b)

    length = property(get_length)

    def __str__(self) -> str:
        return str(f"({self.a}, {self.b})")

    def __getitem__(self, index) -> float:
        if index == 0:
            return self.a
        elif index == 1:
            return self.b
        else:
            raise IndexError


class Path:
    def __init__(
            self,
            coord_list: Sequence[tuple[float, float]],
            z: float = 0
                 ):
        """Construct a path of sequences based on a list of coordinates.

        Args:
            coord_list (Sequence[tuple[float, float]]): List of x,y
            coordinates.
            z (float, optional): Height of the path. Defaults to 0.
        """

        if len(coord_list) < 2:
            raise ValueError("Must provide at least two coordinates as a \
                of tuples, e.g. [(x1, y1), (x2, y2)]")

        x, y = tuple(zip(*coord_list))

        self.x_list = list(x)
        self.y_list = list(y)

        coord_list = list(zip(x, y))

        self.segments = [
            PathSegment(i, ip1)
            for i, ip1 in
            zip(coord_list, coord_list[1:])
            ]

        self.z = z

        logger.debug("Path created.")

    def get_length(self) -> float:
        return sum([s.length for s in self.segments])

    length = property(get_length)

    def __getitem__(self, index) -> PathSegment:
        return self.segments[index]

    def __str__(self) -> str:
        return str([str(s) for s in self.segments])

    def plot(self, **kwargs):
        """
        Plot the path using matplotlib.
        """
        plt.plot(self.x_list, self.y_list, **kwargs)


def path_from_RT90(
        df: pd.DataFrame,
        east_col: str = "East",
        north_col: str = "North",
        **kwargs
        ) -> Path:
    """Construct a path from East and North formatted coordinates (RT90)
    in a Pandas DataFrame.

    Args:
        df (pandas.DataFrame): DataFrame containing at least the two columns
        noted in the cols argument.
        east_col (str): The column name for the East coordinates.
        north_col (str): The column name for the North coordinates.

    Returns:
        Path: A Path object built from the aquisition coordinates in the
        DataFrame.
    """

    east_arr = np.array(df[east_col]) - min(df[east_col])
    north_arr = np.array(df[north_col]) - min(df[north_col])

    coord_pairs = list(zip(east_arr, north_arr))

    path = Path(coord_pairs, **kwargs)
    logger.debug("Loaded path from provided RT90 coordinates.")
    return path
