import argparse
import logging
import sys

from pandas.errors import ParserError
from yaml import YAMLError

from pg_rad.detector.builder import DetectorBuilder
from pg_rad.exceptions.exceptions import (
    MissingConfigKeyError,
    OutOfBoundsError,
    DimensionError,
    InvalidIsotopeError
)
from pg_rad.logger.logger import setup_logger
from pg_rad.inputparser.parser import ConfigParser
from pg_rad.landscape.director import LandscapeDirector
from pg_rad.plotting.result_plotter import ResultPlotter
from pg_rad.simulator.engine import SimulationEngine


def main():
    parser = argparse.ArgumentParser(
        prog="pg-rad",
        description="Primary Gamma RADiation landscape tool"
    )
    parser.add_argument(
        "--config",
        help="Build from a config file."
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Load and run the test landscape."
    )
    parser.add_argument(
        "--loglevel",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    parser.add_argument(
        "--saveplot",
        action="store_true",
        help="Save the plot or not."
    )

    args = parser.parse_args()
    setup_logger(args.loglevel)
    logger = logging.getLogger(__name__)

    if args.test:
        test_yaml = """
        name: Test landscape
        speed: 8.33
        acquisition_time: 1

        path:
            length: 1000
            segments:
                - straight

        sources:
            test_source:
                activity_MBq: 1000
                position: [500, 100, 0]
                isotope: CS137
        """

        cp = ConfigParser(test_yaml).parse()
        landscape = LandscapeDirector.build_from_config(cp)

        output = SimulationEngine(
            landscape=landscape,
            runtime_spec=cp.runtime,
            sim_spec=cp.options
        ).simulate()

        plotter = ResultPlotter(landscape, output)
        plotter.plot()

    elif args.config:
        try:
            cp = ConfigParser(args.config).parse()
            landscape = LandscapeDirector.build_from_config(cp)
            detector = DetectorBuilder(cp.detector).build()
            output = SimulationEngine(
                landscape=landscape,
                detector=detector,
                runtime_spec=cp.runtime,
                sim_spec=cp.options
            ).simulate()

            plotter = ResultPlotter(landscape, output)
            plotter.plot()
        except (
            MissingConfigKeyError,
            KeyError,
            YAMLError,
        ):
            logger.critical(
                "The provided config file is invalid. "
                "Check the log above. You can consult the documentation for "
                "an explanation of how to define a config file."
                )
            sys.exit(1)
        except (
            OutOfBoundsError,
            DimensionError,
            InvalidIsotopeError,
            ValueError
        ) as e:
            logger.critical(e)
            logger.critical(
                "One or more items in config are not specified correctly. "
                "Please consult this log and fix the problem."
                )
            sys.exit(1)

        except (
            FileNotFoundError,
            ParserError
        ):
            sys.exit(1)


if __name__ == "__main__":
    main()
