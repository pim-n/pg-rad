import logging
import os
from typing import Any, Dict, List, Union

import yaml

from pg_rad.exceptions.exceptions import MissingConfigKeyError, DimensionError
from pg_rad.configs import defaults

from .specs import (
    MetadataSpec,
    RuntimeSpec,
    SimulationOptionsSpec,
    SegmentSpec,
    PathSpec,
    ProceduralPathSpec,
    CSVPathSpec,
    SourceSpec,
    AbsolutePointSourceSpec,
    RelativePointSourceSpec,
    SimulationSpec,
)


logger = logging.getLogger(__name__)


class ConfigParser:
    _ALLOWED_ROOT_KEYS = {
        "name",
        "speed",
        "acquisition_time",
        "path",
        "sources",
        "options",
    }

    def __init__(self, config_source: str):
        self.config = self._load_yaml(config_source)

    def parse(self) -> SimulationSpec:
        self._warn_unknown_keys(
            section="global",
            provided=set(self.config.keys()),
            allowed=self._ALLOWED_ROOT_KEYS,
        )

        metadata = self._parse_metadata()
        runtime = self._parse_runtime()
        options = self._parse_options()
        path = self._parse_path()
        sources = self._parse_point_sources()

        return SimulationSpec(
            metadata=metadata,
            runtime=runtime,
            options=options,
            path=path,
            point_sources=sources,
        )

    # ----------------------------------------------------------

    def _load_yaml(self, config_source: str) -> Dict[str, Any]:
        if os.path.exists(config_source):
            with open(config_source) as f:
                return yaml.safe_load(f)
        return yaml.safe_load(config_source)

    # ----------------------------------------------------------

    def _parse_metadata(self) -> MetadataSpec:
        try:
            return MetadataSpec(
                name=self.config["name"]
            )
        except KeyError as e:
            raise MissingConfigKeyError("global", {"name"}) from e

    # ----------------------------------------------------------

    def _parse_runtime(self) -> RuntimeSpec:
        required = {"speed", "acquisition_time"}
        missing = required - self.config.keys()
        if missing:
            raise MissingConfigKeyError("global", missing)

        return RuntimeSpec(
            speed=float(self.config["speed"]),
            acquisition_time=float(self.config["acquisition_time"]),
        )

    # ----------------------------------------------------------

    def _parse_options(self) -> SimulationOptionsSpec:
        options = self.config.get("options", {})

        allowed = {"air_density", "seed"}
        self._warn_unknown_keys(
            section="options",
            provided=set(options.keys()),
            allowed=allowed,
        )

        return SimulationOptionsSpec(
            air_density=float(options.get(
                "air_density",
                defaults.DEFAULT_AIR_DENSITY
                )),
            seed=options.get("seed"),
        )

    # ----------------------------------------------------------

    def _parse_path(self) -> PathSpec:
        allowed_csv = {"file", "east_col_name", "north_col_name", "z"}
        allowed_proc = {"segments", "length", "z"}

        if "path" not in self.config:
            raise MissingConfigKeyError("global", {"path"})

        path = self.config["path"]

        if "file" in path:
            self._warn_unknown_keys(
                section="path (csv)",
                provided=set(path.keys()),
                allowed=allowed_csv,
            )

            return CSVPathSpec(
                file=path["file"],
                east_col_name=path["east_col_name"],
                north_col_name=path["north_col_name"],
                z=path.get("z", 0),
            )

        if "segments" in path:
            self._warn_unknown_keys(
                section="path (procedural)",
                provided=set(path.keys()),
                allowed=allowed_proc,
            )
            return self._parse_procedural_path(path)

        raise ValueError("Invalid path configuration.")

    # ----------------------------------------------------------

    def _parse_procedural_path(
        self,
        path: Dict[str, Any]
    ) -> ProceduralPathSpec:
        raw_segments = path["segments"]
        raw_length = path.get("length")

        if raw_length is None:
            raise MissingConfigKeyError("path", {"length"})

        if isinstance(raw_length, int | float):
            raw_length = [float(raw_length)]

        segments = self._process_segment_angles(raw_segments)
        lengths = self._process_segment_lengths(raw_length, len(segments))
        resolved_segments = self._combine_segments_lengths(segments, lengths)

        return ProceduralPathSpec(
            segments=resolved_segments,
            z=path.get("z", defaults.DEFAULT_PATH_HEIGHT),
        )

    def _process_segment_angles(
        self,
        raw_segments: List[Union[str, dict]]
    ) -> List[Dict[str, Any]]:

        normalized = []

        for segment in raw_segments:

            if isinstance(segment, str):
                normalized.append({"type": segment, "angle": None})

            elif isinstance(segment, dict):
                if len(segment) != 1:
                    raise ValueError("Invalid segment definition.")
                seg_type, angle = list(segment.items())[0]
                normalized.append({"type": seg_type, "angle": angle})

            else:
                raise ValueError("Invalid segment entry format.")

        return normalized

    def _process_segment_lengths(
        self,
        raw_length_list: List[Union[int, float]],
        num_segments: int
    ) -> List[float]:
        num_lengths = len(raw_length_list)

        if num_lengths == num_segments:
            return raw_length_list
        elif num_lengths == 1:
            length_list = raw_length_list + [None] * (num_segments - 1)
            return length_list
        else:
            raise ValueError(
                "Path length must either be a single number or a list with "
                "number of elements equal to the number of segments."
            )

    def _combine_segments_lengths(
        self,
        segments: List[Dict[str, Any]],
        lengths: List[float],
    ) -> List[SegmentSpec]:

        resolved = []

        for seg, length in zip(segments, lengths):
            angle = seg["angle"]

            if angle is not None and not self._is_turn(seg["type"]):
                raise ValueError(
                    f"A {seg["type"]} segment does not support an angle."
                )

            resolved.append(
                SegmentSpec(
                    type=seg["type"],
                    length=length,
                    angle=angle,
                )
            )

        return resolved

    @staticmethod
    def _is_turn(segment_type: str) -> bool:
        return segment_type in {"turn_left", "turn_right"}

    def _parse_point_sources(self) -> List[SourceSpec]:
        source_dict = self.config.get("sources", {})
        specs: List[SourceSpec] = []

        for name, params in source_dict.items():

            required = {"activity_MBq", "isotope", "position"}
            missing = required - params.keys()
            if missing:
                raise MissingConfigKeyError(name, missing)

            position = params["position"]

            if isinstance(position, list):
                if len(position) != 3:
                    raise DimensionError(
                        "Absolute position must be [x, y, z]."
                    )

                specs.append(
                    AbsolutePointSourceSpec(
                        name=name,
                        activity_MBq=float(params["activity_MBq"]),
                        isotope=params["isotope"],
                        x=float(position[0]),
                        y=float(position[1]),
                        z=float(position[2]),
                    )
                )

            elif isinstance(position, dict):
                specs.append(
                    RelativePointSourceSpec(
                        name=name,
                        activity_MBq=float(params["activity_MBq"]),
                        isotope=params["isotope"],
                        along_path=float(position["along_path"]),
                        dist_from_path=float(position["dist_from_path"]),
                        side=position["side"],
                        z=position.get("z", defaults.DEFAULT_SOURCE_HEIGHT)
                    )
                )

            else:
                raise ValueError(
                    f"Invalid position format for source '{name}'."
                    )

        return specs

    def _warn_unknown_keys(self, section: str, provided: set, allowed: set):
        unknown = provided - allowed
        if unknown:
            logger.warning(
                f"Unknown keys in '{section}' section: {unknown}"
            )
