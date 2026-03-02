import logging

import pandas as pd


logger = logging.getLogger(__name__)


def load_data(filename: str) -> pd.DataFrame:
    logger.debug(f"Attempting to load file: {filename}")

    try:
        df = pd.read_csv(filename, delimiter=',')
    except FileNotFoundError as e:
        logger.critical(e)
        raise
    except pd.errors.ParserError as e:
        logger.critical(e)
        raise

    logger.debug(f"File loaded: {filename}")
    return df
