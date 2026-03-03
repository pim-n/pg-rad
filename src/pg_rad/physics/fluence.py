from typing import Tuple, TYPE_CHECKING

import numpy as np

from pg_rad.detector.detectors import IsotropicDetector, AngularDetector


if TYPE_CHECKING:
    from pg_rad.landscape.landscape import Landscape


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
    mu_mass_air *= 0.1
    mu_air = mu_mass_air * air_density

    phi_r = (
        activity
        * eff
        * branching_ratio
        * np.exp(-mu_air * r)
        / (4 * np.pi * r**2)
    )

    return phi_r


def calculate_fluence_at(
    landscape: "Landscape",
    pos: np.ndarray,
    detector: IsotropicDetector | AngularDetector,
    tangent_vectors: np.ndarray,
    scaling=1E6
):
    """Compute fluence at an arbitrary position in the landscape.

    Args:
        landscape (Landscape): The landscape to compute.
        pos (np.ndarray): (N, 3) array of positions.
        detector (IsotropicDetector | AngularDetector):
            Detector object, needed to compute correct efficiency.

    Returns:
        total_phi (np.ndarray): (N,) array of fluences.
    """
    pos = np.atleast_2d(pos)
    total_phi = np.zeros(pos.shape[0])

    for source in landscape.point_sources:
        source_to_detector = pos - np.array(source.pos)
        r = np.linalg.norm(source_to_detector, axis=1)
        r = np.maximum(r, 1E-3)  # enforce minimum distance of 1cm

        if isinstance(detector, AngularDetector):
            cos_theta = (
                np.sum(tangent_vectors * source_to_detector, axis=1) / (
                    np.linalg.norm(source_to_detector, axis=1) *
                    np.linalg.norm(tangent_vectors, axis=1)
                )
            )
            cos_theta = np.clip(cos_theta, -1, 1)
            theta = np.arccos(cos_theta)
            eff = detector.get_efficiency(theta, energy=source.isotope.E)
        else:
            eff = detector.get_efficiency(energy=source.isotope.E)

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


def calculate_fluence_along_path(
    landscape: "Landscape",
    detector: "IsotropicDetector | AngularDetector",
    points_per_segment: int = 10
) -> Tuple[np.ndarray, np.ndarray]:
    path = landscape.path
    num_points = len(path.x_list)

    dx = np.diff(path.x_list)
    dy = np.diff(path.y_list)
    segment_lengths = np.sqrt(dx**2 + dy**2)

    original_distances = np.zeros(num_points)
    original_distances[1:] = np.cumsum(segment_lengths)

    # arc lengths at which to evaluate the path
    s = np.linspace(
        0,
        original_distances[-1],
        num=num_points * points_per_segment)

    # Interpolate x and y as functions of arc length
    xnew = np.interp(s, original_distances, path.x_list)
    ynew = np.interp(s, original_distances, path.y_list)
    z = np.full(xnew.shape, path.z)
    full_positions = np.c_[xnew, ynew, z]

    # to compute the angle between sources and the direction of travel, we
    # compute tangent vectors along the path.
    dx_ds = np.gradient(xnew, s)
    dy_ds = np.gradient(ynew, s)
    tangent_vectors = np.c_[dx_ds, dy_ds, np.zeros_like(dx_ds)]
    tangent_vectors /= np.linalg.norm(tangent_vectors, axis=1, keepdims=True)

    phi_result = calculate_fluence_at(
        landscape,
        full_positions,
        detector,
        tangent_vectors)

    return s, phi_result
