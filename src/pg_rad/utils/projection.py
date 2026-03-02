from typing import List, Tuple

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


def minimal_distance_to_path(
    x_list: List[float],
    y_list: List[float],
    path_z: float,
    pos: Tuple[float, float, float]
) -> float:
    """
    Compute minimal Euclidean distance from pos (x,y,z)
    to interpolated polyline path at height path_z.
    """
    x, y, z = pos

    path = np.column_stack((x_list, y_list))
    point_xy = np.array([x, y])

    segments = np.diff(path, axis=0)
    segment_lengths = np.hypot(segments[:, 0], segments[:, 1])

    min_dist = np.inf

    for p0, seg, seg_len in zip(path[:-1], segments, segment_lengths):
        if seg_len == 0:
            continue

        t = np.dot(point_xy - p0, seg) / (seg_len ** 2)
        t = np.clip(t, 0.0, 1.0)

        projection_xy = p0 + t * seg

        dx, dy = point_xy - projection_xy
        dz = z - path_z

        dist = np.sqrt(dx**2 + dy**2 + dz**2)

        if dist < min_dist:
            min_dist = dist

    return min_dist


def abs_to_rel_source_position(
    x_list: List,
    y_list: List,
    path_z: int | float,
    pos: Tuple[float, float, float],
) -> Tuple[float, float, str, float]:
    """
    Convert absolute (x,y,z) position into:
        along_path,
        dist_from_path,
        side ("left" or "right"),
        z_rel
    """

    x, y, z = pos

    path = np.column_stack((x_list, y_list))
    point = np.array([x, y])

    segments = np.diff(path, axis=0)
    segment_lengths = np.hypot(segments[:, 0], segments[:, 1])

    arc_length = np.cumsum(segment_lengths)
    arc_length = np.insert(arc_length, 0, 0)

    min_dist = np.inf
    best_projection = None
    best_s_i = None
    best_fraction = None
    best_signed_dist = None

    for (i, (p0, seg, seg_len)) in enumerate(
        zip(path[:-1], segments, segment_lengths)
    ):
        if seg_len == 0:
            continue

        # project point onto infinite line
        t = np.dot(point - p0, seg) / (seg_len ** 2)

        # clamp to segment
        t_clamped = np.clip(t, 0.0, 1.0)

        projection = p0 + t_clamped * seg
        diff_vec = point - projection
        dist = np.linalg.norm(diff_vec)

        if dist < min_dist:
            min_dist = dist
            best_projection = projection
            best_s_i = i
            best_fraction = t_clamped

            # tangent and perpendicular
            tangent_vec = seg / seg_len
            perp_vec = np.array([-tangent_vec[1], tangent_vec[0]])

            signed_dist = np.dot(diff_vec, perp_vec)
            best_signed_dist = signed_dist

    if best_projection is None:
        raise ValueError("Could not project point onto path.")

    # Compute along_path
    along_path = (
        arc_length[best_s_i] + best_fraction * segment_lengths[best_s_i]
    )

    # Side and distance
    side = "left" if best_signed_dist > 0 else "right"
    dist_from_path = abs(best_signed_dist)

    # z relative
    z_rel = z - path_z

    return along_path, dist_from_path, side, z_rel
