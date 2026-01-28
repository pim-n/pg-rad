class ConvergenceError(Exception):
    """Raised when an algorithm fails to converge."""

class DataLoadError(Exception):
    """Base class for data loading errors."""

class InvalidCSVError(DataLoadError):
    """Raised when a file is not a valid CSV."""