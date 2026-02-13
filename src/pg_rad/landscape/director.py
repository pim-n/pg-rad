from importlib.resources import files
import logging

from pg_rad.configs.filepaths import TEST_EXP_DATA
from pg_rad.isotopes import CS137
from pg_rad.landscape.landscape import LandscapeBuilder
from pg_rad.objects import PointSource


class LandscapeDirector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("LandscapeDirector initialized.")

    def build_test_landscape(self):
        fp = files('pg_rad.data').joinpath(TEST_EXP_DATA)
        source = PointSource(activity=100E9, isotope=CS137(), pos=(0, 0, 0))
        lb = LandscapeBuilder("Test landscape")
        lb.set_air_density(1.243)
        lb.set_path_from_experimental_data(fp, z=0)
        lb.set_point_sources(source)
        landscape = lb.build()
        return landscape
