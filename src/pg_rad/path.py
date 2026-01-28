from collections.abc import Sequence
import math

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import piecewise_regression

from pg_rad.exceptions import ConvergenceError
from pg_rad.logger import setup_logger

logger = setup_logger(__name__)

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
            z: float = 0,
            path_simplify = False
                 ):
        """Construct a path of sequences based on a list of coordinates.

        Args:
            coord_list (Sequence[tuple[float, float]]): List of x,y coordinates.
            z (float, optional): Height of the path. Defaults to 0.
            path_simplify (bool, optional): Whether to pg_rad.path.simplify_path(). Defaults to False.
        """        
        
        if len(coord_list) < 2:
            raise ValueError("Must provide at least two coordinates as a list of tuples, e.g. [(x1, y1), (x2, y2)]")

        x, y = tuple(zip(*coord_list))
    
        if path_simplify:
            try:
                x, y = simplify_path(list(x), list(y))
            except ConvergenceError:
                logger.warning("Continuing without simplifying path.")

        self.x_list = list(x)
        self.y_list = list(y)

        coord_list = list(zip(x, y))

        self.segments = [PathSegment(i, ip1) for i, ip1 in zip(coord_list, coord_list[1:])]

        self.z = z

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

def simplify_path(
        x: Sequence[float],
        y: Sequence[float],
        keep_endpoints_equal: bool = False,
        n_breakpoints: int = 3
        ):
    """From full resolution x and y arrays, return a piecewise linearly approximated/simplified pair of x and y arrays.

    This function uses the `piecewise_regression` package. From a full set of
    coordinate pairs, the function fits linear sections, automatically finding
    the number of breakpoints and their positions.

    On why the default value of n_breakpoints is 3, from the `piecewise_regression`
    docs:
    "If you do not have (or do not want to use) initial guesses for the number
    of breakpoints, you can set it to n_breakpoints=3, and the algorithm will
    randomly generate start_values. With a 50% chance, the bootstrap restarting
    algorithm will either use the best currently converged breakpoints or
    randomly generate new start_values, escaping the local optima in two ways in
    order to find better global optima."

    Args:
        x (Sequence[float]): Full list of x coordinates.
        y (Sequence[float]): Full list of y coordinates.
        keep_endpoints_equal (bool, optional): Whether or not to force start
        and end to be exactly equal to the original. This will worsen the linear
        approximation at the beginning and end of path. Defaults to False.
        n_breakpoints (int, optional): Number of breakpoints. Defaults to 3.

    Returns:
        x (list[float]): Reduced list of x coordinates.
        y (list[float]): Reduced list of y coordinates.

    Raises:
        ConvergenceError: If the fitting algorithm failed to simplify the path.

    Reference:
        Pilgrim, C., (2021). piecewise-regression (aka segmented regression) in Python. Journal of Open Source Software, 6(68), 3859, https://doi.org/10.21105/joss.03859.
    """
    
    logger.debug(f"Attempting piecewise regression on path.")

    pw_fit = piecewise_regression.Fit(x, y, n_breakpoints=n_breakpoints)
    pw_res = pw_fit.get_results()

    if pw_res == None:
        logger.error("Piecewise regression failed to converge.")
        raise ConvergenceError("Piecewise regression failed to converge.") 
    
    est = pw_res['estimates']

    # extract and sort breakpoints
    breakpoints_x = sorted(
        v['estimate'] for k, v in est.items() if k.startswith('breakpoint')
    )
 
    x_points = [x[0]] + breakpoints_x + [x[-1]]

    y_points = pw_fit.predict(x_points)

    if keep_endpoints_equal:
        logger.debug("Forcing endpoint equality.")
        y_points[0] = y[0]
        y_points[-1] = y[-1]

    logger.info(
        f"Piecewise regression reduced path from {len(x)-1} to {len(x_points)-1} segments."
    )

    return x_points, y_points

def path_from_RT90(
        df: pd.DataFrame,
        east_col: str = "East",
        north_col: str = "North",
        **kwargs
        ) -> Path:
    """Construct a path from East and North formatted coordinates (RT90) in a Pandas DataFrame.

    Args:
        df (pandas.DataFrame): DataFrame containing at least the two columns noted in the cols argument.
        east_col (str): The column name for the East coordinates.
        north_col (str): The column name for the North coordinates.

    Returns:
        Path: A Path object built from the aquisition coordinates in the DataFrame.
    """    
    
    east_arr = np.array(df[east_col]) - min(df[east_col])
    north_arr = np.array(df[north_col]) - min(df[north_col])

    coord_pairs = list(zip(east_arr, north_arr))

    path = Path(coord_pairs, **kwargs)
    return path