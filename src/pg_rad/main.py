import argparse

from pg_rad.logger import setup_logger
from pg_rad.landscape import LandscapeDirector


def main():
    parser = argparse.ArgumentParser(
        prog="pg-rad",
        description="Primary Gamma RADiation landscape tool"
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

    args = parser.parse_args()
    setup_logger(args.loglevel)

    if args.test:
        landscape = LandscapeDirector().build_test_landscape()
        print(landscape.name)


if __name__ == "__main__":
    main()
