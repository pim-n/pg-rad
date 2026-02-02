import math
from typing import Self

class BaseObject:
    def __init__(
            self,
            x: float,
            y: float,
            z: float,
            name: str = "Unnamed object",
            color: str = 'grey'):
        """
        A generic object.

        Args:
            x (float): X coordinate.
            y (float): Y coordinate.
            z (float): Z coordinate.
            name (str, optional): Name for the object. Defaults to "Unnamed object".
            color (str, optional): Matplotlib compatible color string. Defaults to "red".
        """
        
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