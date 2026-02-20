import logging

from .objects import BaseObject
from pg_rad.isotopes.isotope import Isotope, get_isotope

logger = logging.getLogger(__name__)


class PointSource(BaseObject):
    _id_counter = 1

    def __init__(
            self,
            activity_MBq: int,
            isotope: str,
            position: tuple[float, float, float] = (0, 0, 0),
            name: str | None = None,
            color: str = 'red'
            ):
        """A point source.

        Args:
            activity_MBq (int): Activity A in MBq.
            isotope (Isotope): The isotope.
            pos (tuple[float, float, float], optional):
                Position of the PointSource.
            name (str, optional): Can give the source a unique name.
                If not provided, point sources are sequentially
                named: Source1, Source2, ...
            color (str, optional): Matplotlib compatible color string
        """

        self.id = PointSource._id_counter
        PointSource._id_counter += 1

        # default name derived from ID if not provided
        if name is None:
            name = f"Source {self.id}"

        super().__init__(position, name, color)

        self.activity = activity_MBq
        self.isotope: Isotope = get_isotope(isotope)

        logger.debug(f"Source created: {self.name}")

    def __repr__(self):
        x, y, z = self.position
        repr_str = (f"PointSource(name={self.name}, "
                    + f"pos={(x, y, z)}, "
                    + f"A={self.activity} MBq), "
                    + f"isotope={self.isotope.name}.")

        return repr_str
