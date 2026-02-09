from math import dist, exp, pi

import pytest

from pg_rad.isotopes import CS137
from pg_rad.landscape import Landscape
from pg_rad.objects import PointSource


@pytest.fixture
def phi_ref():
    A = 100                             # MBq
    b = 0.851
    mu_mass_air = 0.0778                # cm^2/g
    air_density = 1.243                 # kg/m^3
    r = dist((0, 0, 0), (10, 10, 0))    # m

    A *= 1E9                            # Convert to Bq
    mu_mass_air *= 0.1                  # Convert to m^2/kg

    mu_air = mu_mass_air * air_density  # [m^2/kg] x [kg/m^3] = [m^-1]

    # [s^-1] x exp([m^-1] x [m]) / [m^-2] = [s^-1 m^-2]
    phi = A * b * exp(-mu_air * r) / (4 * pi * r**2)
    return phi


@pytest.fixture
def test_landscape():
    landscape = Landscape()
    source = PointSource(
        pos=(0, 0, 0),
        activity=100E9,
        isotope=CS137)
    landscape.add_sources(source)
    return landscape


def test_single_source_fluence(phi_ref, test_landscape):
    phi = test_landscape.calculate_fluence_at((10, 10, 0))
    assert pytest.approx(phi, rel=1E-3) == phi_ref
