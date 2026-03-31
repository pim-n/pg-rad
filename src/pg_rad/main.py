import argparse
import logging
import sys

from pandas.errors import ParserError

from pg_rad.exceptions.exceptions import (
    MissingConfigKeyError,
    OutOfBoundsError,
    DimensionError,
    InvalidConfigValueError,
    InvalidIsotopeError,
    InvalidYAMLError
)
from pg_rad.logger.logger import setup_logger
from pg_rad.inputparser.parser import ConfigParser
from pg_rad.landscape.director import LandscapeDirector
from pg_rad.plotting.result_plotter import ResultPlotter
from pg_rad.simulator.engine import SimulationEngine
from pg_rad.utils.export import generate_folder_name, save_results


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
        "--example",
        action="store_true",
        help="Load and run an example landscape."
    )
    parser.add_argument(
        "--loglevel",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    parser.add_argument(
        "--showplots",
        action="store_true",
        help="Show the plots immediately."
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the outputs"
    )

    args = parser.parse_args()
    setup_logger(args.loglevel)
    logger = logging.getLogger(__name__)

    if args.example:
        input_config = """
        name: Example landscape
        speed: 8.33
        acquisition_time: 1

        path:
            length:
                - 500
                - 500
            segments:
                - straight
                - turn_left: 45
            direction: negative

        sources:
            test_source:
                activity_MBq: 100
                position: [250, 30, 0]
                isotope: Cs137
                gamma_energy_keV: 661

        detector: LU_NaI_3inch
        """
    elif args.config:
        input_config = args.config

    try:
        cp = ConfigParser(input_config).parse()
        landscape = LandscapeDirector.build_from_config(cp)
        output = SimulationEngine(
            landscape=landscape,
            runtime_spec=cp.runtime,
            sim_spec=cp.options
        ).simulate()

        plotter = ResultPlotter(landscape, output)
        if args.save:
            folder_name = generate_folder_name(output)
            save_results(output, folder_name)
            plotter.save(folder_name)
        if args.showplots:
            plotter.plot()

    except (
        MissingConfigKeyError,
        KeyError
    ) as e:
        logger.critical(e)
        logger.critical(
            "The config file is missing required keys or may be an "
            "invalid YAML file. Check the log above. Consult the "
            "documentation for examples of how to write a config file."
            )
        sys.exit(1)
    except (
        OutOfBoundsError,
        DimensionError,
        InvalidIsotopeError,
        InvalidConfigValueError,
        NotImplementedError
    ) as e:
        logger.critical(e)
        logger.critical(
            "One or more items in config are not specified correctly. "
            "Please consult this log and fix the problem."
            )
        sys.exit(1)

    except (
        FileNotFoundError,
        ParserError,
        InvalidYAMLError
    ) as e:
        logger.critical(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
