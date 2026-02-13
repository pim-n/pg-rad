class ConvergenceError(Exception):
    """Raised when an algorithm fails to converge."""


class DataLoadError(Exception):
    """Base class for data loading errors."""


class InvalidCSVError(DataLoadError):
    """Raised when a file is not a valid CSV."""


class OutOfBoundsError(Exception):
    """Raised when an object is attempted to be placed out of bounds."""
