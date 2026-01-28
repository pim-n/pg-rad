import logging
import logging.config
import pathlib

import yaml

def setup_logger(name):
    logger = logging.getLogger(name)

    base_dir = pathlib.Path(__file__).resolve().parent
    config_file = base_dir / "configs" / "logging.yml"

    with open(config_file) as f:
        config = yaml.safe_load(f)
    
    logging.config.dictConfig(config)
    return logger