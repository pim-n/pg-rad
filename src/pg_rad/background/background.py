from importlib.resources import files
from typing import Tuple
import numpy as np
from pandas import read_csv

from pg_rad.configs.defaults import FWHM_PARAMS
from pg_rad.detector.detector import Detector


def generate_background(
    cps_array: np.ndarray,
) -> np.ndarray:
    """
    Generate synthetic background cps for a given detector and energy.
    """
    pass


def fwhm(A: float, B: float, C: float, E: float) -> float:
    return np.sqrt(A + B * E + C * E**2)


def get_roi_from_fwhm(
    detector: Detector,
    energy_keV: float
) -> Tuple[float, float]:
    """
    Get the region of interest for given primary gamma energy, using
    the 3*FWHM rule.
    """
    A, B, C = FWHM_PARAMS.get(detector.type)
    delta = 3*fwhm(A, B, C, energy_keV)
    return (energy_keV-delta, energy_keV+delta)


def get_cps_from_roi(
    detector: Detector,
    roi_lo: float,
    roi_hi: float
) -> float:

    csv = files('pg_rad.data.backgrounds').joinpath(detector.name+'.csv')
    data = read_csv(csv)

    # get indices of nearest bins
    idx_min = (data["Energy"] - roi_lo).abs().idxmin()
    idx_max = (data["Energy"] - roi_hi).abs().idxmin()
    idx_start, idx_end = sorted([idx_min, idx_max])

    cps_sum = data.loc[idx_start:idx_end, "cps"].sum()
    return cps_sum
