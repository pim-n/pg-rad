from typing import Tuple, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from pg_rad.landscape.landscape import Landscape


def phi(
        r: float,
        activity: float | int,
        branching_ratio: float,
        mu_mass_air: float,
        air_density: float,
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
        * branching_ratio
        * np.exp(-mu_air * r)
        / (4 * np.pi * r**2)
    )

    return phi_r


def calculate_fluence_at(landscape: "Landscape", pos: np.ndarray):
    """Compute fluence at an arbitrary position in the landscape.

    Args:
        landscape (Landscape): The landscape to compute.
        pos (np.ndarray): (N, 3) array of positions.

    Returns:
        total_phi (np.ndarray): (N,) array of fluences.
    """
    total_phi = np.zeros(pos.shape[0])

    for source in landscape.point_sources:
        r = np.linalg.norm(pos - np.array(source.pos), axis=1)
        r = np.maximum(r, 1e-3)  # enforce minimum distance of 1cm

        phi_source = phi(
            r=r,
            activity=source.activity,
            branching_ratio=source.isotope.b,
            mu_mass_air=source.isotope.mu_mass_air,
            air_density=landscape.air_density
        )

        total_phi += phi_source

    return total_phi


def calculate_fluence_along_path(
    landscape: "Landscape",
    points_per_segment: int = 10
) -> Tuple[np.ndarray, np.ndarray]:
    path = landscape.path
    num_segments = len(path.segments)

    xnew = np.linspace(
        path.x_list[0],
        path.x_list[-1],
        num=num_segments*points_per_segment)

    ynew = np.interp(xnew, path.x_list, path.y_list)

    z = np.full(xnew.shape, path.z)
    full_positions = np.c_[xnew, ynew, z]
    phi_result = calculate_fluence_at(landscape, full_positions)

    dist_travelled = np.linspace(
        full_positions[0, 0],
        path.length,
        len(phi_result)
    )

    return dist_travelled, phi_result
