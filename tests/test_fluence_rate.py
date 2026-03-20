import numpy as np
import pytest

from pg_rad.inputparser.parser import ConfigParser
from pg_rad.landscape.director import LandscapeDirector
from pg_rad.physics.fluence import phi


@pytest.fixture
def isotropic_detector():
    from pg_rad.detector.detector import load_detector
    return load_detector('dummy')


@pytest.fixture
def phi_ref(test_landscape, isotropic_detector):
    source = test_landscape.point_sources[0]

    r = np.linalg.norm(np.array([0, 0, 0]) - np.array(source.pos))

    A = source.activity * 1E6
    b = source.isotope.b
    mu_air = source.isotope.mu_mass_air * test_landscape.air_density
    mu_air *= 0.1

    eff = isotropic_detector.get_efficiency(source.isotope.E)
    return A * eff * b * np.exp(-mu_air * r) / (4 * np.pi * r**2)


@pytest.fixture
def test_landscape():

    test_yaml = """
    name: Test landscape
    speed: 8.33
    acquisition_time: 1

    path:
        length: 1000
        segments:
            - straight

    sources:
        test_source:
            activity_MBq: 100
            position: [0, 100, 0]
            isotope: Cs137
            gamma_energy_keV: 661

    detector: dummy
    """

    cp = ConfigParser(test_yaml).parse()
    landscape = LandscapeDirector.build_from_config(cp)
    return landscape


def test_single_source_fluence(phi_ref, test_landscape, isotropic_detector):
    s = test_landscape.point_sources[0]
    r = np.linalg.norm(np.array([0, 0, 0]) - np.array(s.pos))
    phi_calc = phi(
        r,
        s.activity*1E6,
        s.isotope.b,
        s.isotope.mu_mass_air,
        test_landscape.air_density,
        isotropic_detector.get_efficiency(s.isotope.E)
        )

    assert pytest.approx(phi_calc, rel=1E-6) == phi_ref
