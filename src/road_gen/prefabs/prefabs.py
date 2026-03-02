import numpy as np


def straight(length: int) -> np.ndarray:
    return np.zeros(length)


def turn_left(length: int, radius: float) -> np.ndarray:
    return np.full(length, 1.0 / radius)


def turn_right(length: int, radius: float) -> np.ndarray:
    return -turn_left(length, radius)


PREFABS = {
    'straight': straight,
    'turn_left': turn_left,
    'turn_right': turn_right,
}
