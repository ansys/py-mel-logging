"""py-mel-logging."""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

# from .python_logger_provider import PythonLoggerProvider
from .python_logger import PythonLogger
