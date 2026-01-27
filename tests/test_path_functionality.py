import pathlib

import numpy as np
import pytest

from pg_rad.dataloader import load_data
from pg_rad.path import Path, path_from_RT90

@pytest.fixture
def test_df():
    csv_path = pathlib.Path(__file__).parent / "data/coordinates.csv"
    return load_data(csv_path)

def test_piecewise_regression(test_df):
    """_Verify whether the intermediate points deviate less than 0.1 SD._"""
        
    p_full = path_from_RT90(
        test_df,
        east_col="East",
        north_col="North",
        simplify_path=False
    )
 
    p_simpl = path_from_RT90(
        test_df,
        east_col="East",
        north_col="North",
        simplify_path=True
    )

    x_f = np.array(p_full.x_list)
    y_f = np.array(p_full.y_list)

    x_s = np.array(p_simpl.x_list)
    y_s = np.array(p_simpl.y_list)

    sd = np.std(y_f)

    for xb, yb in zip(x_s[1:-1], y_s[1:-1]):
        # find nearest original x index
        idx = np.argmin(np.abs(x_f - xb))
        deviation = abs(yb - y_f[idx])

        assert deviation < 0.1 * sd, (
            f"Breakpoint deviation too large: {deviation:.4f} "
            f"(threshold {0.1 * sd:.4f}) at x={xb:.2f}"
            )