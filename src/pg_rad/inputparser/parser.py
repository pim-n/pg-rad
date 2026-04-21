import logging
import os
from typing import Any, Dict, List, Union

import yaml

from pg_rad.exceptions.exceptions import (
    MissingConfigKeyError,
    DimensionError,
    InvalidConfigValueError,
    InvalidYAMLError
)
from pg_rad.configs import defaults
from pg_rad.isotopes.isotope import get_isotope

from .specs import (
    MetadataSpec,
    RuntimeSpec,
    SimulationOptionsSpec,
    PathSpec,
    ProceduralPathSpec,
    CSVPathSpec,
    PointSourceSpec,
    AbsolutePointSourceSpec,
    RelativePointSourceSpec,
    DetectorSpec,
    SimulationSpec
)


logger = logging.getLogger(__name__)


class ConfigParser:
    _ALLOWED_ROOT_KEYS = {
        "name",
        "speed",
        "acquisition_time",
        "path",
        "sources",
        "detector",
        "options"
    }

    def __init__(self, config_source: str):
        self.config = self._load_yaml(config_source)

    def parse(self) -> SimulationSpec:
        self._warn_unknown_keys(
            section="root",
            provided=set(self.config.keys()),
            allowed=self._ALLOWED_ROOT_KEYS,
        )

        metadata = self._parse_metadata()
        runtime = self._parse_runtime()
        options = self._parse_options()
        path = self._parse_path()
        sources = self._parse_point_sources()
        detector = self._parse_detector()

        return SimulationSpec(
            metadata=metadata,
            runtime=runtime,
            options=options,
            path=path,
            point_sources=sources,
            detector=detector
        )

    def _load_yaml(self, config_source: str) -> Dict[str, Any]:
        if os.path.exists(config_source):
            with open(config_source) as f:
                data = yaml.safe_load(f)
        else:
            data = yaml.safe_load(config_source)

        if not isinstance(data, dict):
            raise InvalidYAMLError(
                "Provided path or string is not a valid YAML representation."
            )

        return data

    def _parse_metadata(self) -> MetadataSpec:
        try:
            return MetadataSpec(
                name=self.config["name"]
            )
        except KeyError as e:
            raise MissingConfigKeyError("root", {"name"}) from e

    def _parse_runtime(self) -> RuntimeSpec:
        required = {"speed", "acquisition_time"}
        missing = required - self.config.keys()
        if missing:
            raise MissingConfigKeyError("root", missing)

        return RuntimeSpec(
            speed=float(self.config["speed"]),
            acquisition_time=float(self.config["acquisition_time"]),
        )

    def _parse_options(self) -> SimulationOptionsSpec:
        options = self.config.get("options", {})

        allowed = {"air_density_kg_per_m3", "seed", "bkg_cps"}
        self._warn_unknown_keys(
            section="options",
            provided=set(options.keys()),
            allowed=allowed,
        )

        air_density = options.get(
            "air_density_kg_per_m3",
            defaults.DEFAULT_AIR_DENSITY
        )
        seed = options.get("seed")
        bkg_cps = options.get("bkg_cps")

        if not isinstance(air_density, float) or air_density <= 0:
            raise InvalidConfigValueError(
                "options.air_density_kg_per_m3 must be a positive float "
                "in kg/m^3."
            )

        if (
            seed is not None or
            (isinstance(seed, int) and seed <= 0)
        ):
            raise InvalidConfigValueError(
                "Seed must be a positive integer value."
            )

        if bkg_cps is not None and (
            not isinstance(bkg_cps, int) or bkg_cps < 0
        ):
            raise InvalidConfigValueError(
                "Background CPS must be an integer >= 0."
            )

        return SimulationOptionsSpec(
            air_density=air_density,
            seed=seed,
            bkg_cps=bkg_cps
        )

    def _parse_path(self) -> PathSpec:
        allowed_csv = {"file", "east_col_name", "north_col_name", "z"}
        allowed_proc = {"segments", "length", "z", "alpha", "direction"}

        path = self.config.get("path")

        direction = path.get("direction", 'positive')

        if direction == 'positive':
            opposite_direction = False
        elif direction == 'negative':
            opposite_direction = True
        else:
            raise InvalidConfigValueError(
                "Direction must be positive or negative."
            )

        if path is None:
            raise MissingConfigKeyError("path")

        if not isinstance(path, dict):
            raise InvalidConfigValueError("Path must be a dictionary.")

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
                opposite_direction=opposite_direction
            )

        elif "segments" in path:
            self._warn_unknown_keys(
                section="path (procedural)",
                provided=set(path.keys()),
                allowed=allowed_proc,
            )
            return self._parse_procedural_path(path, opposite_direction)

        else:
            raise InvalidConfigValueError("Invalid path configuration.")

    def _parse_procedural_path(
        self,
        path: Dict[str, Any],
        opposite_direction: bool
    ) -> ProceduralPathSpec:
        raw_segments = path.get("segments")

        if not isinstance(raw_segments, List):
            raise InvalidConfigValueError(
                "path.segments must be a list of segments."
            )

        raw_length = path.get("length")

        if raw_length is None:
            raise MissingConfigKeyError("path", {"length"})

        if isinstance(raw_length, int | float):
            raw_length = [float(raw_length)]

        segments, angles = self._process_segment_angles(raw_segments)
        lengths = self._process_segment_lengths(raw_length, len(segments))

        return ProceduralPathSpec(
            segments=segments,
            angles=angles,
            lengths=lengths,
            z=path.get("z", defaults.DEFAULT_PATH_HEIGHT),
            alpha=path.get("alpha", defaults.DEFAULT_ALPHA),
            opposite_direction=opposite_direction
        )

    def _process_segment_angles(
        self,
        raw_segments: List[Union[str, dict]]
    ) -> List[Dict[str, Any]]:

        segments, angles = [], []

        for segment in raw_segments:

            if isinstance(segment, str):
                segments.append(segment)
                angles.append(None)

            elif isinstance(segment, dict):
                if len(segment) != 1:
                    raise InvalidConfigValueError(
                        "Invalid segment definition."
                    )
                seg_type, angle = list(segment.items())[0]
                segments.append(seg_type)
                angles.append(angle)

            else:
                raise InvalidConfigValueError(
                    "Invalid segment entry format."
                )

        return segments, angles

    def _process_segment_lengths(
        self,
        raw_length_list: List[Union[int, float]],
        num_segments: int
    ) -> List[float]:
        num_lengths = len(raw_length_list)

        if num_lengths == num_segments or num_lengths == 1:
            return raw_length_list
        else:
            raise ValueError(
                "Path length must either be a single number or a list with "
                "number of elements equal to the number of segments."
            )

    @staticmethod
    def _is_turn(segment_type: str) -> bool:
        return segment_type in {"turn_left", "turn_right"}

    def _parse_point_sources(self) -> List[PointSourceSpec]:
        source_dict = self.config.get("sources")
        if source_dict is None:
            raise MissingConfigKeyError("sources")

        if not isinstance(source_dict, dict):
            raise InvalidConfigValueError(
                "sources must have subkeys representing point source names."
            )

        specs: List[PointSourceSpec] = []

        for name, params in source_dict.items():
            required = {
                "activity_MBq", "isotope", "position", "gamma_energy_keV"
            }
            if not isinstance(params, dict):
                raise InvalidConfigValueError(
                    f"sources.{name} is not defined correctly."
                    f" Must have subkeys {required}"
                )

            missing = required - params.keys()
            if missing:
                raise MissingConfigKeyError(name, missing)

            activity = params.get("activity_MBq")
            isotope_name = params.get("isotope")
            gamma_energy_keV = params.get("gamma_energy_keV")

            isotope = get_isotope(isotope_name, gamma_energy_keV)

            if not isinstance(activity, int | float) or activity <= 0:
                raise InvalidConfigValueError(
                    f"sources.{name}.activity_MBq must be positive value "
                    "in MegaBequerels."
                )

            position = params.get("position")

            if isinstance(position, list):
                if len(position) != 3:
                    raise DimensionError(
                        "Absolute position must be [x, y, z]."
                    )

                specs.append(
                    AbsolutePointSourceSpec(
                        name=name,
                        activity_MBq=float(activity),
                        isotope=isotope,
                        x=float(position[0]),
                        y=float(position[1]),
                        z=float(position[2]),
                    )
                )

            elif isinstance(position, dict):
                alignment = position.get("acquisition_alignment")
                if alignment not in {'best', 'worst', None}:
                    raise InvalidConfigValueError(
                        f"sources.{name}.acquisition_alignment must be "
                        "'best' or 'worst', with 'best' aligning source "
                        f"{name} in the middle of the two nearest acquisition "
                        "points, and 'worst' aligning exactly perpendicular "
                        "to the nearest acquisition point."
                    )

                specs.append(
                    RelativePointSourceSpec(
                        name=name,
                        activity_MBq=float(activity),
                        isotope=isotope,
                        along_path=float(position["along_path"]),
                        dist_from_path=float(position["dist_from_path"]),
                        side=position["side"],
                        z=position.get("z", defaults.DEFAULT_SOURCE_HEIGHT),
                        alignment=alignment
                    )
                )

            else:
                raise InvalidConfigValueError(
                    f"Invalid position format for source '{name}'."
                    )

        return specs

    def _parse_detector(self) -> DetectorSpec:
        det_name = self.config.get("detector")
        if not det_name:
            raise MissingConfigKeyError("detector")

        return DetectorSpec(name=det_name)

    def _warn_unknown_keys(self, section: str, provided: set, allowed: set):
        unknown = provided - allowed
        if unknown:
            logger.warning(
                f"Unknown keys in '{section}' section: {unknown}"
            )
