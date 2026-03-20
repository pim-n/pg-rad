import pytest

from pg_rad.background.background import get_roi_from_fwhm, get_cps_from_roi
from pg_rad.detector.detector import load_detector

E_gamma = 661.7  # keV


@pytest.fixture
def detector():
    return load_detector("LU_NaI_3inch")


@pytest.fixture
def roi_Cs137_NaI(detector):
    return get_roi_from_fwhm(detector, E_gamma)


@pytest.mark.parametrize("ref_roi_lo, ref_roi_hi", [
    (537.58, 792.69)
])
def test_roi_acquisition_Cs137_NaI(ref_roi_lo, ref_roi_hi, roi_Cs137_NaI):
    """Test against ROI used in GammaVision"""
    est_roi_lo, est_roi_hi = roi_Cs137_NaI

    assert pytest.approx(est_roi_lo, rel=0.05) == ref_roi_lo
    assert pytest.approx(est_roi_hi, rel=0.05) == ref_roi_hi


@pytest.mark.parametrize("ref_cps", [
    13.61
])
def test_cps_acquisition_Cs137_NaI(
    ref_cps,
    roi_Cs137_NaI,
    detector
):
    """Test against cps from GammaVision"""
    est_roi_lo, est_roi_hi = roi_Cs137_NaI
    est_cps = get_cps_from_roi(detector, est_roi_lo, est_roi_hi)

    assert pytest.approx(est_cps, rel=0.1) == ref_cps
