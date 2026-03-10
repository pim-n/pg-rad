from importlib.resources import files
import logging

from pg_rad.configs.filepaths import TEST_EXP_DATA
from .builder import LandscapeBuilder
from pg_rad.inputparser.specs import (
    SimulationSpec,
    CSVPathSpec,
    ProceduralPathSpec
)
from pg_rad.objects.sources import PointSource


logger = logging.getLogger(__name__)


class LandscapeDirector:
    def __init__(self):
        logger.debug("LandscapeDirector initialized.")

    @staticmethod
    def build_test_landscape():
        fp = files('pg_rad.data').joinpath(TEST_EXP_DATA)
        source = PointSource(
            activity_MBq=100E6,
            isotope="CS137",
            position=(0, 0, 0)
        )
        lb = LandscapeBuilder("Test landscape")
        lb.set_air_density(1.243)
        lb.set_path_from_experimental_data(fp, z=0)
        lb.set_point_sources(source)
        landscape = lb.build()
        return landscape

    @staticmethod
    def build_from_config(config: SimulationSpec):
        lb = LandscapeBuilder(config.metadata.name)
        lb.set_air_density(config.options.air_density)

        if isinstance(config.path, CSVPathSpec):
            lb.set_path_from_experimental_data(spec=config.path)
        elif isinstance(config.path, ProceduralPathSpec):
            lb.set_path_from_segments(
                sim_spec=config,
            )
        lb.set_point_sources(*config.point_sources)
        lb.set_detector(config.detector)
        landscape = lb.build()
        return landscape
