class ConvergenceError(Exception):
    """Raised when an algorithm fails to converge."""


class DataLoadError(Exception):
    """Base class for data loading errors."""


class InvalidCSVError(DataLoadError):
    """Raised when a file is not a valid CSV."""


class OutOfBoundsError(Exception):
    """Raised when an object is attempted to be placed out of bounds."""


class MissingConfigKeyError(KeyError):
    """Raised when a (nested) config key is missing in the config."""
    def __init__(self, key, subkey=None):
        if subkey:
            self.message = f"Missing key in {key}: {', '.join(list(subkey))}"
        else:
            self.message = f"Missing key: {key}"

        super().__init__(self.message)


class DimensionError(ValueError):
    """Raised if dimensions or coordinates do not match the system."""


class InvalidIsotopeError(ValueError):
    """Raised if attempting to load an isotope that is not valid."""


class InvalidConfigValueError(ValueError):
    """Raised if a config key has an incorrect type or value."""
