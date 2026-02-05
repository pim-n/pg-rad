import logging

from .objects import BaseObject
from pg_rad.isotopes import Isotope

logger = logging.getLogger(__name__)


class PointSource(BaseObject):
    _id_counter = 1

    def __init__(
            self,
            x: float,
            y: float,
            z: float,
            activity: int,
            isotope: Isotope,
            name: str | None = None,
            color: str = "red"):
        """A point source.

        Args:
            x (float): X coordinate.
            y (float): Y coordinate.
            z (float): Z coordinate.
            activity (int): Activity A in MBq.
            isotope (Isotope): The isotope.
            name (str | None, optional): Can give the source a unique name.
            Defaults to None, making the name sequential.
            (Source-1, Source-2, etc.).
            color (str, optional): Matplotlib compatible color string.
            Defaults to "red".
        """

        self.id = PointSource._id_counter
        PointSource._id_counter += 1

        # default name derived from ID if not provided
        if name is None:
            name = f"Source {self.id}"

        super().__init__(x, y, z, name, color)

        self.activity = activity
        self.isotope = isotope
        self.color = color

        logger.debug(f"Source created: {self.name}")

    def __repr__(self):
        repr_str = (f"PointSource(name={self.name}, "
                    + f"pos={(self.x, self.y, self.z)}, "
                    + f"A={self.activity} MBq), "
                    + f"isotope={self.isotope.name}.")

        return repr_str
