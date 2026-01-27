import math
from typing import Self

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
    def __init__(
            self,
            x: float,
            y: float,
            z: float,
            strength: int,
            name: str = "Unnamed source",
            color: str = "red"):
    
        super().__init__(x, y, z, name, color)

        self.strength = strength
        self.color = color

    def __repr__(self):
        return f"Source(name={self.name}, strength={self.strength}, pos={(self.x, self.y, self.z)})"