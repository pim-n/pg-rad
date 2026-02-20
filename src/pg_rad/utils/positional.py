from typing import List

import numpy as np

from pg_rad.exceptions.exceptions import OutOfBoundsError


def rel_to_abs_source_position(
    x_list: List,
    y_list: List,
    path_z: int | float,
    along_path: int | float,
    side: str,
    dist_from_path: int | float,
    z_rel: int | float = 0
):
    path = np.column_stack((x_list, y_list))
    segments = np.diff(path, axis=0)
    segment_lengths = np.hypot(segments[:, 0], segments[:, 1])

    arc_length = np.cumsum(segment_lengths)
    arc_length = np.insert(arc_length, 0, 0)

    # find index of the segment where the source should be placed
    s_i = np.searchsorted(arc_length, along_path, side='right') - 1
    if not 0 <= s_i < len(segments):
        raise OutOfBoundsError(
            "along_path must be less than the length of the path!"
            )

    # fraction of segment length where to place the point source
    segment_fraction = (
        (along_path - arc_length[s_i])
        / segment_lengths[s_i]
    )

    # tangential vector at point where point source to be placed
    point_on_path = path[s_i] + segment_fraction * segments[s_i]
    tangent_vec = segments[s_i] / segment_lengths[s_i]

    if side not in {"left", "right"}:
        raise ValueError("side must be 'left' or 'right'")

    orientation = 1 if side == "left" else -1
    perp_vec = orientation * np.array([-tangent_vec[1], tangent_vec[0]])

    x_abs, y_abs = point_on_path + dist_from_path * perp_vec
    z_abs = path_z + z_rel

    return x_abs, y_abs, z_abs
