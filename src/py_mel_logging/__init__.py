"""py-mel-logging."""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata  # type: ignore

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

from .load_dotnet_python_logging import load_dotnet_python_logging
from .python_logger_provider import create_logger_provider
from .python_logger import PythonLogger
