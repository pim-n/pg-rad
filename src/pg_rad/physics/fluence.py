from typing import Tuple, TYPE_CHECKING

import numpy as np

from pg_rad.background.background import generate_background

if TYPE_CHECKING:
    from pg_rad.landscape.landscape import Landscape
    from pg_rad.detector.detector import Detector


def phi(
        r: float,
        activity: float | int,
        branching_ratio: float,
        mu_mass_air: float,
        air_density: float,
        eff: float
        ) -> float:
    """Compute the contribution of a single point source to the
    primary photon fluence rate phi at position (x,y,z).

    Args:
        r (float): [m] Distance to the point source.
        activity (float | int): [Bq] Activity of the point source.
        branching_ratio (float): Branching ratio for the photon energy E_gamma.
        mu_mass_air (float): [cm^2/g] Mass attenuation coefficient for air.
        air_density (float): [kg/m^3] Air density.

    Returns:
        phi (float): [s^-1 m^-2] Primary photon fluence rate at distance r from
        a point source.
    """

    # Linear photon attenuation coefficient in m^-1.
    mu_air = 0.1 * mu_mass_air * air_density

    phi_r = (
        activity
        * eff
        * branching_ratio
        * np.exp(-mu_air * r)
    ) / (4 * np.pi * r**2)

    return phi_r


def calculate_count_rate_per_second(
    landscape: "Landscape",
    pos: np.ndarray,
    detector: "Detector",
    scaling=1E6
):
    """Compute count rate in s^-1 m^-2 at a position in the landscape.

    Args:
        landscape (Landscape): The landscape to compute.
        pos (np.ndarray): (N, 3) array of positions.
        detector (Detector):
            Detector object, needed to compute correct efficiency.

    Returns:
        total_phi (np.ndarray): (N,) array of count rates per second.
    """
    pos = np.atleast_2d(pos)
    total_phi = np.zeros(pos.shape[0])

    for source in landscape.point_sources:
        # See Bukartas (2021) page 25 for incidence angle math
        source_to_detector = pos - np.array(source.pos)
        r = np.linalg.norm(source_to_detector, axis=1)
        r = np.maximum(r, 1E-3)  # enforce minimum distance of 1cm

        if not detector.is_isotropic:
            v = np.zeros_like(pos)
            v[1:] = pos[1:] - pos[:-1]
            v[0] = v[1]  # handle first point
            vx, vy = v[:, 0], v[:, 1]

            r_vec = pos - np.array(source.pos)
            rx, ry = r_vec[:, 0], r_vec[:, 1]

            theta = np.arctan2(vy, vx) - np.arctan2(ry, rx)

            # normalise to [-pi, pi] and convert to degrees
            theta = (theta + np.pi) % (2 * np.pi) - np.pi
            theta_deg = np.degrees(theta)

            eff = detector.get_efficiency(source.isotope.E, theta_deg)
        else:
            eff = detector.get_efficiency(source.isotope.E)

        phi_source = phi(
            r=r,
            activity=source.activity * scaling,
            branching_ratio=source.isotope.b,
            mu_mass_air=source.isotope.mu_mass_air,
            air_density=landscape.air_density,
            eff=eff
        )

        total_phi += phi_source

    return total_phi


def calculate_counts_along_path(
    landscape: "Landscape",
    detector: "Detector",
    velocity: float,
    points_per_segment: int = 10,
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute the counts recorded in each acquisition period in the landscape.

    Args:
        landscape (Landscape): _description_
        detector (Detector): _description_
        points_per_segment (int, optional): _description_. Defaults to 100.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Array of acquisition points and
            integrated count rates.
    """

    path = landscape.path
    num_points = len(path.x_list)
    num_segments = len(path.segments)

    segment_lengths = np.array([seg.length for seg in path.segments])
    original_distances = np.zeros(num_points)
    original_distances[1:] = np.cumsum(segment_lengths)

    # arc lengths at which to evaluate the path
    total_subpoints = num_segments * points_per_segment
    s = np.linspace(0, original_distances[-1], total_subpoints)

    # Interpolate x and y as functions of arc length
    xnew = np.interp(s, original_distances, path.x_list)
    ynew = np.interp(s, original_distances, path.y_list)
    z = np.full_like(xnew, path.z)
    full_positions = np.c_[xnew, ynew, z]

    if path.opposite_direction:
        full_positions = np.flip(full_positions, axis=0)

    # [counts/s]
    cps = calculate_count_rate_per_second(
        landscape, full_positions, detector
    )

    bkg = generate_background(
        cps, detector, landscape.point_sources[0].isotope.E
    )

    cps_with_bg = cps + bkg
    # reshape so each segment is on a row
    cps_per_seg = cps_with_bg.reshape(num_segments, points_per_segment)

    du = s[1] - s[0]
    integrated_counts = np.trapezoid(cps_per_seg, dx=du, axis=1) / velocity
    int_counts_result = np.zeros(num_points)
    int_counts_result[1:] = integrated_counts

    return original_distances, s, cps_with_bg, int_counts_result, np.mean(bkg)
