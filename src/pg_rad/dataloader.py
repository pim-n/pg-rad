import logging

import pandas as pd

from pg_rad.exceptions import DataLoadError, InvalidCSVError

logger = logging.getLogger(__name__)

def load_data(filename: str) -> pd.DataFrame:
    logger.debug(f"Attempting to load file: {filename}")

    try:
        df = pd.read_csv(filename, delimiter=',')

    except FileNotFoundError as e:
        logger.error(f"File not found: {filename}")
        raise DataLoadError(f"File does not exist: {filename}") from e

    except pd.errors.ParserError as e:
        logger.error(f"Invalid CSV format: {filename}")
        raise InvalidCSVError(f"Invalid CSV file: {filename}") from e

    except Exception as e:
        logger.exception(f"Unexpected error while loading {filename}")
        raise DataLoadError("Unexpected error while loading data") from e

    logger.debug(f"File loaded: {filename}")
    return df