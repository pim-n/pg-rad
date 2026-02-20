class ConvergenceError(Exception):
    """Raised when an algorithm fails to converge."""


class DataLoadError(Exception):
    """Base class for data loading errors."""


class InvalidCSVError(DataLoadError):
    """Raised when a file is not a valid CSV."""


class OutOfBoundsError(Exception):
    """Raised when an object is attempted to be placed out of bounds."""


class MissingNestedKeyError(Exception):
    """Raised when a nested key is missing in the config."""
    def __init__(self, key, subkey=None):
        if subkey:
            self.message = f"Missing key in {key}: {subkey}"
        else:
            self.message = f"Missing key: {key}"

        super().__init__(self.message)
