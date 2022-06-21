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

clr.AddReference("Microsoft.Extensions.DependencyInjection")
clr.AddReference("Microsoft.Extensions.Logging")
clr.AddReference("Microsoft.Extensions.Logging.Abstractions")
clr.AddReference("Python.Runtime")
import Microsoft.Extensions.DependencyInjection as DependencyInjection  # type: ignore
from Microsoft.Extensions.Logging import EventId, LogLevel, ILogger
from System import Object
from Python.Logging import DotNetPythonLogger, PythonLoggerExtensions


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


def test_use_in_dotnet():
    # Setup
    result = StringIO()
    handler = logging.StreamHandler(result)
    handler.setLevel(logging.DEBUG)

    provider: PythonLoggerProvider = create_logger_provider(logging.WARN, handler)
    sc = DependencyInjection.ServiceCollection()
    PythonLoggerExtensions.ConfigureServiceCollection(sc, provider)
    sp = DependencyInjection.ServiceCollectionContainerBuilderExtensions.BuildServiceProvider(sc)

    # SUT
    logger = DependencyInjection.ServiceProviderServiceExtensions.GetRequiredService[
        ILogger[Object]
    ](sp)
    logger.Log[str](LogLevel.Warning, EventId(0), "Eyy", None, None)

    # Verification
    handler.flush()
    assert result.getvalue() == "[0] : Eyy\n"


def test_level_v_level_critical_critical_critical():
    _test_level_v_level(logging.CRITICAL, logging.CRITICAL, LogLevel.Critical, True)


def test_level_v_level_error_error_critical():
    _test_level_v_level(logging.ERROR, logging.ERROR, LogLevel.Critical, True)


def test_level_v_level_critical_critical_error():
    _test_level_v_level(logging.CRITICAL, logging.CRITICAL, LogLevel.Error, False)


def test_level_v_level_error_error_error():
    _test_level_v_level(logging.ERROR, logging.ERROR, LogLevel.Error, True)


def test_level_v_level_warning_warning_error():
    _test_level_v_level(logging.WARNING, logging.WARNING, LogLevel.Error, True)


def test_level_v_level_critical_critical_warning():
    _test_level_v_level(logging.CRITICAL, logging.CRITICAL, LogLevel.Warning, False)


def test_level_v_level_error_error_warning():
    _test_level_v_level(logging.ERROR, logging.ERROR, LogLevel.Warning, False)


def test_level_v_level_warning_warning_warning():
    _test_level_v_level(logging.WARNING, logging.WARNING, LogLevel.Warning, True)


def test_level_v_level_info_info_warning():
    _test_level_v_level(logging.INFO, logging.INFO, LogLevel.Warning, True)


def test_level_v_level_error_error_information():
    _test_level_v_level(logging.ERROR, logging.ERROR, LogLevel.Information, False)


def test_level_v_level_warning_warning_information():
    _test_level_v_level(logging.WARNING, logging.WARNING, LogLevel.Information, False)


def test_level_v_level_info_info_information():
    _test_level_v_level(logging.INFO, logging.INFO, LogLevel.Information, True)


def test_level_v_level_debug_debug_information():
    _test_level_v_level(logging.DEBUG, logging.DEBUG, LogLevel.Information, True)


def test_level_v_level_warning_warning_debug():
    _test_level_v_level(logging.WARNING, logging.WARNING, LogLevel.Debug, False)


def test_level_v_level_info_info_debug():
    _test_level_v_level(logging.INFO, logging.INFO, LogLevel.Debug, False)


def test_level_v_level_debug_debug_debug():
    _test_level_v_level(logging.DEBUG, logging.DEBUG, LogLevel.Debug, True)


def test_level_v_level_info_info_trace():
    _test_level_v_level(logging.INFO, logging.INFO, LogLevel.Trace, False)


def test_level_v_level_debug_debug_trace():
    _test_level_v_level(logging.DEBUG, logging.DEBUG, LogLevel.Trace, False)


def test_level_v_level_debug_minus1_debug_minus1_trace():
    _test_level_v_level(logging.DEBUG - 1, logging.DEBUG - 1, LogLevel.Trace, True)


# handler or provider level can filter
def test_level_v_level_critical_plus1_critical_critical():
    _test_level_v_level(logging.CRITICAL + 1, logging.CRITICAL, LogLevel.Critical, False)


def test_level_v_level_critical_critical_plus1_critical():
    _test_level_v_level(logging.CRITICAL, logging.CRITICAL + 1, LogLevel.Critical, False)


def test_level_v_level_critical_error_error():
    _test_level_v_level(logging.CRITICAL, logging.ERROR, LogLevel.Error, False)


def test_level_v_level_error_critical_error():
    _test_level_v_level(logging.ERROR, logging.CRITICAL, LogLevel.Error, False)


def test_level_v_level_error_warning_warning():
    _test_level_v_level(logging.ERROR, logging.WARNING, LogLevel.Warning, False)


def test_level_v_level_warning_error_warning():
    _test_level_v_level(logging.WARNING, logging.ERROR, LogLevel.Warning, False)


def test_level_v_level_warning_info_information():
    _test_level_v_level(logging.WARNING, logging.INFO, LogLevel.Information, False)


def test_level_v_level_info_warning_information():
    _test_level_v_level(logging.INFO, logging.WARNING, LogLevel.Information, False)


def test_level_v_level_info_debug_debug():
    _test_level_v_level(logging.INFO, logging.DEBUG, LogLevel.Debug, False)


def test_level_v_level_debug_info_debug():
    _test_level_v_level(logging.DEBUG, logging.INFO, LogLevel.Debug, False)


def test_level_v_level_debug_debug_minus1_trace():
    _test_level_v_level(logging.DEBUG, logging.DEBUG - 1, LogLevel.Trace, False)


def test_level_v_level_debug_minus1_debug_trace():
    _test_level_v_level(logging.DEBUG - 1, logging.DEBUG, LogLevel.Trace, False)


def _test_level_v_level(
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
