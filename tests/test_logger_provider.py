"""Tests for create_logger_provider."""
import logging
import os
from io import StringIO

import pytest
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


@pytest.mark.parametrize(
    "handler_level,provider_level,dotnet_log_level,expect_message",
    [
        # handler and provider at same level, equal or more critical pass
        pytest.param(logging.CRITICAL, logging.CRITICAL, LogLevel.Critical, True),
        pytest.param(logging.ERROR, logging.ERROR, LogLevel.Critical, True),
        pytest.param(logging.CRITICAL, logging.CRITICAL, LogLevel.Error, False),
        pytest.param(logging.ERROR, logging.ERROR, LogLevel.Error, True),
        pytest.param(logging.WARNING, logging.WARNING, LogLevel.Error, True),
        pytest.param(logging.CRITICAL, logging.CRITICAL, LogLevel.Warning, False),
        pytest.param(logging.ERROR, logging.ERROR, LogLevel.Warning, False),
        pytest.param(logging.WARNING, logging.WARNING, LogLevel.Warning, True),
        pytest.param(logging.INFO, logging.INFO, LogLevel.Warning, True),
        pytest.param(logging.ERROR, logging.ERROR, LogLevel.Information, False),
        pytest.param(logging.WARNING, logging.WARNING, LogLevel.Information, False),
        pytest.param(logging.INFO, logging.INFO, LogLevel.Information, True),
        pytest.param(logging.DEBUG, logging.DEBUG, LogLevel.Information, True),
        pytest.param(logging.WARNING, logging.WARNING, LogLevel.Debug, False),
        pytest.param(logging.INFO, logging.INFO, LogLevel.Debug, False),
        pytest.param(logging.DEBUG, logging.DEBUG, LogLevel.Debug, True),
        pytest.param(logging.INFO, logging.INFO, LogLevel.Trace, False),
        pytest.param(logging.DEBUG, logging.DEBUG, LogLevel.Trace, False),
        pytest.param(logging.DEBUG - 1, logging.DEBUG - 1, LogLevel.Trace, True),
        # handler or provider level can filter
        pytest.param(logging.CRITICAL + 1, logging.CRITICAL, LogLevel.Critical, False),
        pytest.param(logging.CRITICAL, logging.CRITICAL + 1, LogLevel.Critical, False),
        pytest.param(logging.CRITICAL, logging.ERROR, LogLevel.Error, False),
        pytest.param(logging.ERROR, logging.CRITICAL, LogLevel.Error, False),
        pytest.param(logging.ERROR, logging.WARNING, LogLevel.Warning, False),
        pytest.param(logging.WARNING, logging.ERROR, LogLevel.Warning, False),
        pytest.param(logging.WARNING, logging.INFO, LogLevel.Information, False),
        pytest.param(logging.INFO, logging.WARNING, LogLevel.Information, False),
        pytest.param(logging.INFO, logging.DEBUG, LogLevel.Debug, False),
        pytest.param(logging.DEBUG, logging.INFO, LogLevel.Debug, False),
        pytest.param(logging.DEBUG, logging.DEBUG - 1, LogLevel.Trace, False),
        pytest.param(logging.DEBUG - 1, logging.DEBUG, LogLevel.Trace, False),
    ],
)
def test_level_v_level(
    handler_level: int, provider_level: int, dotnet_log_level: LogLevel, expect_message: bool
):
    """
    Test the levels properly filter or pass the different log messages.

    Parameters
    ----------
    handler_level :
        Log level log handler uses.
    provider_level :
        Log level log provider uses, and thus the log writers use.
    dotnet_log_level :
        Dot-Net Log level the log messages are issued at.
    expect_message :
        Do we expect a log message to be generated into the handler.
    """
    result = StringIO()
    handler = logging.StreamHandler(result)
    handler.setLevel(handler_level)
    provider: PythonLoggerProvider = create_logger_provider(provider_level, handler)
    logger: DotNetPythonLogger = provider.CreateLogger("loggerName")
    exception = None
    formatter = None

    # SUT
    logger.Log[str](dotnet_log_level, EventId(42), "Message", exception, formatter)

    # Verify
    handler.flush()
    expected_message = "[42] : Message\n" if expect_message else ""
    assert result.getvalue() == expected_message
