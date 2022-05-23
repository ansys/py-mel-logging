"""Tests for create_logger_provider."""
import logging
import os
import sys
from io import StringIO

sys.path.append(os.path.abspath(os.getcwd() + r"/../dlls/netstandard2.0"))

from clr_loader import get_coreclr

test_path = os.getcwd()
rt = get_coreclr(test_path + r"/../config.json")
from pythonnet import set_runtime

set_runtime(rt)
import clr

clr.AddReference(r"PythonLogging")
from Python.Logging import DotNetPythonLogger, PythonLoggerProvider

clr.AddReference(r"Microsoft.Extensions.Logging.Abstractions")
from Microsoft.Extensions.Logging import EventId, LogLevel

from py_mel_logging import create_logger_provider


def test_create_logger_provider():
    # Setup
    result = StringIO()
    handler = logging.StreamHandler(result)
    handler.setLevel(logging.DEBUG)

    # SUT
    provider: PythonLoggerProvider = create_logger_provider(logging.WARN, handler)
    logger: DotNetPythonLogger = provider.CreateLogger("loggerName")
    logger.Log[str](LogLevel.Warning, EventId(0), "Eyy", None, None)

    # Verification
    handler.flush()
    assert result.getvalue() == "[0] : Eyy\n"
