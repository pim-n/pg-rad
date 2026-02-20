from typing import TYPE_CHECKING

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


def calculate_fluence_at(landscape: "Landscape", pos: tuple):
    total_phi = 0.
    for source in landscape.point_sources:
        r = source.distance_to(pos)
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
):
    
    phi_result = []
 
    path = landscape.path
    waypoints = list(zip(path.x_list, path.y_list))

    for w, wp1 in zip(waypoints, waypoints[1:]):
        x_ref, y_ref = zip(w, wp1)
 
        x = np.linspace(x_ref[0], x_ref[1], points_per_segment)
        y = np.interp(x, x_ref, y_ref)
        z = np.full(x.shape, fill_value=path.z)
        
        for pos in zip(x, y, z):
            phi_segment = calculate_fluence_at(landscape, pos)
            phi_result.append(phi_segment)
    
    return phi_result
    