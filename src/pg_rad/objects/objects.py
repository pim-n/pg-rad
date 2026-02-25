from typing import Self

import numpy as np

from pg_rad.exceptions.exceptions import DimensionError


class BaseObject:
    def __init__(
            self,
            pos: tuple[float, float, float] = (0, 0, 0),
            name: str = "Unnamed object",
            color: str = 'grey'):
        """
        A generic object.

        Args:
            pos (tuple[float, float, float]): Position vector (x,y,z).
            name (str, optional): Name for the object.
            Defaults to "Unnamed object".
            color (str, optional): Matplotlib compatible color string.
            Defaults to "red".
        """

        if len(pos) != 3:
            raise DimensionError("Position must be tuple of length 3 (x,y,z).")
        self.pos = pos
        self.name = name
        self.color = color

    def distance_to(self, other: Self | tuple) -> float:
        if isinstance(other, tuple) and len(other) == 3:
            r = np.linalg.norm(
                np.subtract(self.pos, other)
                )
        else:
            try:
                r = np.linalg.norm(
                    np.subtract(self.pos, other.pos)
                    )
            except AttributeError as e:
                raise e("other must be an object in the world \
                    or a position tuple (x,y,z).")
        return r
