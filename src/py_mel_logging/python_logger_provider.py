"""Implementation of PythonLoggerProvider."""
import logging
import os
import sys

import clr  # type: ignore

from .python_logger import PythonLogger

clr.AddReference("System")
from System import Func  # type: ignore

sys.path.append(os.path.join(os.path.dirname(__file__), "dlls/netstandard2.0"))
clr.AddReference(r"PythonLogging")
from Python.Logging import PythonLoggerProvider  # type: ignore

clr.AddReference(r"Python.Runtime")
from Python.Runtime import PyObject  # type: ignore


def create_logger_provider(log_level: int, log_handler: logging.Handler) -> PythonLoggerProvider:
    """
    Create a new .Net Microsoft.Extensions.Logging ILoggingProvider \
    that logs using a Python logger with the given logging.Handler.

    Parameters
    ----------
    log_level The log level of the logger to create.
    log_handler The logging handler to use.

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
