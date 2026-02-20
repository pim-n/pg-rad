import argparse
import logging
import sys

from pandas.errors import ParserError
from yaml import YAMLError

from pg_rad.exceptions.exceptions import MissingNestedKeyError
from pg_rad.logger.logger import setup_logger
from pg_rad.landscape.director import LandscapeDirector
from pg_rad.plotting.landscape_plotter import LandscapeSlicePlotter


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
        help="Load and run the test landscape"
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
        landscape = LandscapeDirector().build_test_landscape()
        plotter = LandscapeSlicePlotter()
        plotter.plot(landscape, save=args.saveplot)

    elif args.config:
        try:
            landscape = LandscapeDirector.build_from_config(args.config)
            plotter = LandscapeSlicePlotter()
            plotter.plot(landscape, save=args.saveplot)
        except (
            MissingNestedKeyError,
            KeyError,
            YAMLError
        ):
            logger.critical(
                "The provided config file is invalid. "
                "Check the log above. You can consult the documentation for "
                "an explanation of how to define a config file."
                )
            sys.exit(1)
        except (
            FileNotFoundError,
            ParserError
        ):
            sys.exit(1)


if __name__ == "__main__":
    main()
