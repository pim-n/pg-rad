import logging
import logging.config
import pathlib

import yaml

def setup_logger(log_level: str = "WARNING"):
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    
    if not log_level in levels:
        raise ValueError(f"Log level must be one of {levels}.")
    
    base_dir = pathlib.Path(__file__).resolve().parent
    config_file = base_dir / "configs" / "logging.yml"

    with open(config_file) as f:
        config = yaml.safe_load(f)
    
    config["loggers"]["root"]["level"] = log_level

    logging.config.dictConfig(config)