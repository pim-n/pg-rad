from importlib.resources import files
import logging

from pg_rad.configs.filepaths import TEST_EXP_DATA
from .landscape import LandscapeBuilder
from .config_parser import ConfigParser
from pg_rad.objects.sources import PointSource
from pg_rad.utils.positional import rel_to_abs_source_position


logger = logging.getLogger(__name__)


class LandscapeDirector:
    def __init__(self):
        logger.debug("LandscapeDirector initialized.")

    @staticmethod
    def build_test_landscape():
        fp = files('pg_rad.data').joinpath(TEST_EXP_DATA)
        source = PointSource(activity=100E9, isotope="CS137", pos=(0, 0, 0))
        lb = LandscapeBuilder("Test landscape")
        lb.set_air_density(1.243)
        lb.set_path_from_experimental_data(fp, z=0)
        lb.set_point_sources(source)
        landscape = lb.build()
        return landscape

    @staticmethod
    def build_from_config(path_to_config):
        conf = ConfigParser(path_to_config)
        conf.parse()

        lb = LandscapeBuilder(conf.name)

        if conf.path_type == 'csv':
            lb.set_path_from_experimental_data(**conf.path)
        elif conf.path_type == 'procedural':
            lb.set_path_from_segments(
                speed=conf.speed,
                acquisition_time=conf.acquisition_time,
                **conf.path
            )

        sources = []
        for s_name, s_params in conf.sources.items():
            if isinstance(s_params['position'], dict):
                path = lb.get_path()
                x_abs, y_abs, z_abs = rel_to_abs_source_position(
                    x_list=path.x_list,
                    y_list=path.y_list,
                    path_z=path.z,
                    **s_params['position']
                )

                s_params['position'] = [x_abs, y_abs, z_abs]

            sources.append(PointSource(name=s_name, **s_params))

        lb.set_point_sources(*sources)
        landscape = lb.build()
        return landscape
