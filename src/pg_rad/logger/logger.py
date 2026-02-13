import logging.config
from importlib.resources import files

import yaml

from pg_rad.configs.filepaths import LOGGING_CONFIG


def setup_logger(log_level: str = "WARNING"):
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    if log_level not in levels:
        raise ValueError(f"Log level must be one of {levels}.")

    config_file = files('pg_rad.configs').joinpath(LOGGING_CONFIG)

    with open(config_file) as f:
        config = yaml.safe_load(f)

    config["loggers"]["root"]["level"] = log_level

    logging.config.dictConfig(config)
