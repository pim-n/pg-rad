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


class ColorFormatter(logging.Formatter):
    # ANSI escape codes
    COLORS = {
        logging.DEBUG: "\033[36m",     # Cyan
        logging.INFO: "\033[32m",      # Green
        logging.WARNING: "\033[33m",   # Yellow
        logging.ERROR: "\033[31m",     # Red
        logging.CRITICAL: "\033[41m",  # Red background
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        record.msg = f"{record.msg}"
        return super().format(record)
