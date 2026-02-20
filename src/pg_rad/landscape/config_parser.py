import logging
from typing import Any, Dict, List, Tuple, Union

import yaml

from pg_rad.exceptions.exceptions import MissingNestedKeyError


# used to check required keys that are nested within source
REQUIRED_SOURCE_KEYS = {'activity_MBq', 'isotope', 'position'}


logger = logging.getLogger(__name__)


class ConfigParser:
    def __init__(self, config_path: str):
        try:
            with open(config_path) as f:
                self.config = yaml.safe_load(f)
            logger.debug("YAML config file loaded correctly.")
            self.path_type: str = None
            self.path: Dict = {}
            self.sources: Dict[str, Dict[str, Any]] = {}
        except FileNotFoundError as e:
            logger.critical(f"Config file not found: {e}")
            raise
        except yaml.YAMLError as e:
            logger.critical(f"Error parsing YAML file: {e}")
            raise

    def parse(self) -> None:
        try:
            self._parse_required()
            logger.debug("Global keys parsed.")
            self._parse_path()
            logger.debug("Path parsed.")
            self._parse_point_sources()
            logger.debug("Point sources parsed.")
        except (MissingNestedKeyError, KeyError) as e:
            logger.critical(e)
            raise

    def _parse_required(self) -> None:
        logger.debug("Attempting to parse the required global keys.")
        self.name = self.config['name']
        self.speed = self.config['speed']
        self.acquisition_time = self.config['acquisition_time']
        self.ds = self.speed * self.acquisition_time

    def _parse_path(self) -> None:
        logger.debug("Attempting to parse the path.")
        path = self.config['path']

        if path.get('file'):
            logger.debug("Experimental CSV path detected in config file.")
            self.path_type = "csv"
            self.path = path
        elif path.get('segments'):
            logger.debug("Procedural path detected in config file.")
            self.path_type = "procedural"

            length = path.get('length')
            segments, angles = self._parse_segment_list(
                    path.get('segments')
            )

            if (
                isinstance(length, list)
                and len(length) != len(segments)
            ):
                raise ValueError(
                    "the path.length subkey must either be a single number "
                    "(e.g. length: 100) representing the total length of the "
                    "path, or a list corresponding to each segment in "
                    "path.segments."
                    )

            self.path.update({
                'segments': segments,
                'length': length,
                'angles': angles
            })

    def _parse_point_sources(self) -> None:
        """Parse point sources configuration."""
        logger.debug("Attempting to parse the point sources.")
        source_dict = self.config.get('sources')
        if source_dict:
            for source, params in source_dict.items():
                diff = REQUIRED_SOURCE_KEYS - set(params)
                if diff:
                    raise MissingNestedKeyError(source, diff)

                self.sources[source] = params

        else:
            logger.info("No point sources provided.")

    @staticmethod
    def _parse_segment_list(
        input_segments: List[Union[str, dict]]
    ) -> Tuple[List[str], List[float | None]]:
        """
        The segments list is a list of segments and possible angles.
        """
        segments = []
        angles = []

        for s in input_segments:
            if isinstance(s, str):
                segments.append(s)
                angles.append(None)
            elif isinstance(s, dict):
                seg_name, seg_angle = list(s.items())[0]
                segments.append(seg_name)
                angles.append(seg_angle)

        return segments, angles
