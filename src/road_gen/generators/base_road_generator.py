import secrets

import numpy as np


class BaseRoadGenerator:
    """A base generator object for generating a road of a specified length."""
    def __init__(
            self,
            length: int | float,
            ds: int | float,
            velocity: int | float,
            mu: float = 0.7,
            g: float = 9.81,
            seed: int | None = None
            ):
        """Initialize a BaseGenerator with a given or random seed.

        Args:
            length (int | float): The total length of the road in meters.
            ds (int | float): The step size in meters.
            velocity (int | float): Velocity in meters per second.
            mu (float): Coefficient of friction. Defaults to 0.7 (dry asphalt).
            g (float): Acceleration due to gravity (m/s^2). Defaults to 9.81.
            seed (int | None, optional): Set a seed for the generator.
                Defaults to a random seed.
        """
        if seed is None:
            seed = secrets.randbits(32)

        if not isinstance(seed, int):
            raise TypeError("seed must be an integer or None.")

        if not isinstance(length, int | float):
            raise TypeError("Length must be an integer or float in meters.")

        if not isinstance(ds, int | float):
            raise TypeError("Step size must be integer or float in meters.")

        if not isinstance(velocity, int | float):
            raise TypeError(
                "Velocity must be integer or float in meters per second."
            )

        self.length = length
        self.ds = ds

        self.velocity = velocity
        self.min_radius = (velocity ** 2) / (g * mu)

        self.seed = seed
        self._rng = np.random.default_rng(seed)

    def generate(self):
        pass
