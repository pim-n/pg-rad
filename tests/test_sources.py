import numpy as np
import pytest

from pg_rad.sources import PointSource

@pytest.fixture
def test_sources():
    pos_a = np.random.rand(3)
    pos_b = np.random.rand(3)

    a = PointSource(*tuple(pos_a), strength = None)
    b = PointSource(*tuple(pos_b), strength = None)

    return pos_a, pos_b, a, b

def test_if_distances_equal(test_sources):
    """Verify whether from PointSource A to PointSource B is the same as B to A."""

    _, _, a, b = test_sources

    assert a.distance_to(b) == b.distance_to(a)

def test_distance_calculation(test_sources):
    """Verify whether distance between two PointSources is calculated correctly."""

    pos_a, pos_b, a, b = test_sources

    dx = pos_b[0] - pos_a[0]
    dy = pos_b[1] - pos_a[1]
    dz = pos_b[2] - pos_a[2]

    assert np.isclose(
        a.distance_to(b),
        np.sqrt(dx**2 + dy**2 + dz**2),
        rtol = 1e-12)