import math
from typing import Self

from pg_rad.isotope import Isotope

class Object:
    def __init__(
            self,
            x: float,
            y: float,
            z: float,
            name: str = "Unnamed object",
            color: str = 'grey'):
        
        self.x = x
        self.y = y
        self.z = z
        self.name = name
        self.color = color
    
    def distance_to(self, other: Self) -> float:
        return math.dist(
            (self.x, self.y, self.z),
            (other.x, other.y, other.z),
        )
    
class Source(Object):
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
        """_A point source._

        Args:
            x (float): X coordinate.
            y (float): Y coordinate.
            z (float): Z coordinate.
            activity (int): Activity A in MBq.
            isotope (Isotope): The isotope.
            name (str | None, optional): Can give the source a unique name.
            Defaults to None, making the name sequential.
            (Source-1, Source-2, etc.).
            color (str, optional): Matplotlib compatible color string. Defaults to "red".
        """        
        self.id = Source._id_counter
        Source._id_counter += 1

        # default name derived from ID if not provided
        if name is None:
            name = f"Source {self.id}"

        super().__init__(x, y, z, name, color)

        self.activity = activity
        self.isotope = isotope
        self.color = color

    def __repr__(self):
        return f"Source(name={self.name}, pos={(self.x, self.y, self.z)}, isotope={self.isotope.name}, A={self.activity} MBq)"