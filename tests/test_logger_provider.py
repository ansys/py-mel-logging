"""Tests for create_logger_provider."""
import logging
import os
from io import StringIO

from clr_loader import get_coreclr
from py_mel_logging import create_logger_provider
from pythonnet import set_runtime

test_path = os.getcwd()
rt = get_coreclr(test_path + r"/../config.json")
set_runtime(rt)

import clr

clr.AddReference(r"Microsoft.Extensions.Logging.Abstractions")
from Microsoft.Extensions.Logging import EventId, LogLevel


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
