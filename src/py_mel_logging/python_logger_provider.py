"""Implementation of PythonLoggerProvider."""
import logging

import clr  # type: ignore

clr.AddReference("System")
from System import Func  # type: ignore

from .load_dotnet_python_logging import load_dotnet_python_logging

load_dotnet_python_logging()
from Python.Logging import PythonLoggerProvider  # type: ignore

clr.AddReference(r"Python.Runtime")
from Python.Runtime import PyObject  # type: ignore

from .python_logger import PythonLogger


def create_logger_provider(log_level: int, log_handler: logging.Handler) -> PythonLoggerProvider:
    """
    Create a new .Net Microsoft.Extensions.Logging ILoggingProvider \
    that logs using a Python logger with the given logging.Handler.

    Parameters
    ----------
    log_level: int
        The .Net log level of the logger to create.
            0 = Trace,
            1 = Debug,
            2 = Information,
            3 = Warning,
            4 = Error,
            5 = Critical,
            6 = None
    log_handler: logging.Handler
        The logging handler to use.

    Returns
    -------
    A .Net ILoggingProvider that creates loggers that log to a python
    logger.
    """

    def create_logger_func() -> PythonLogger:
        pylogger = PythonLogger(log_level, log_handler)
        return pylogger

    func = Func[PyObject](create_logger_func)
    provider = PythonLoggerProvider(func)
    return provider
