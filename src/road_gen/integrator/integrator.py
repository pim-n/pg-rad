import numpy as np


def integrate_road(curvature: np.ndarray, ds: float = 1.0):
    """Integrate along the curvature field to obtain X and Y coordinates.

    Args:
        curvature (np.ndarray): The curvature field.
        ds (float, optional): _description_. Defaults to 1.0.

    Returns:
        x, y (np.ndarray): X and Y waypoints.
    """

    theta = np.zeros(len(curvature))
    theta[1:] = np.cumsum(curvature[:-1] * ds)

    x = np.cumsum(np.cos(theta) * ds)
    y = np.cumsum(np.sin(theta) * ds)

    return x, y
