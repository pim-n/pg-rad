import pytest

from pg_rad.utils.interpolators import get_mass_attenuation_coeff


@pytest.mark.parametrize("energy,mu", [
    (1.00000E-03, 3.606E+03),
    (1.00000E-02, 5.120E+00),
    (1.00000E-01, 1.541E-01),
    (1.00000E+00, 6.358E-02),
    (1.00000E+01, 2.045E-02)
])
def test_exact_attenuation_retrieval(energy, mu):
    """
    Test if retrieval of values that are exactly in the table is correct.
    """
    func_mu = get_mass_attenuation_coeff(energy)
    assert pytest.approx(func_mu, rel=1E-6) == mu


@pytest.mark.parametrize("energy,mu", [
    (0.662, 0.0778)
])
def test_attenuation_interpolation(energy, mu):
    """
    Test retreival for Cs-137 mass attenuation coefficient.
    """
    interp_mu = get_mass_attenuation_coeff(energy)
    assert pytest.approx(interp_mu, rel=1E-2) == mu
