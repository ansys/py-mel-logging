"""py-mel-logging."""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata  # type: ignore

__version__ = importlib_metadata.version(__name__.replace(".", "-"))


def __import_python_logging() -> None:
    import clr
    import os
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), "dlls/netstandard2.0"))
    clr.AddReference(r"PythonLogging")


__import_python_logging()
from .python_logger_provider import create_logger_provider
from .python_logger import PythonLogger
