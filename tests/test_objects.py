import numpy as np
import pytest

from pg_rad.objects import Source

@pytest.fixture
def test_sources():
    pos_a = np.random.rand(3)
    pos_b = np.random.rand(3)

    a = Source(*tuple(pos_a), strength = None)
    b = Source(*tuple(pos_b), strength = None)

    return pos_a, pos_b, a, b

def test_if_distances_equal(test_sources):
    """_Verify whether from object A to object B is the same as B to A._"""

    _, _, a, b = test_sources

    assert a.distance_to(b) == b.distance_to(a)

def test_distance_calculation(test_sources):
    """_Verify whether distance between two static objects (e.g. sources) 
    is calculated correctly._"""

    pos_a, pos_b, a, b = test_sources

    dx = pos_b[0] - pos_a[0]
    dy = pos_b[1] - pos_a[1]
    dz = pos_b[2] - pos_a[2]

    assert np.isclose(
        a.distance_to(b),
        np.sqrt(dx**2 + dy**2 + dz**2),
        rtol = 1e-12)