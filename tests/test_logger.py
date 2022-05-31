"""Tests for PythonLogger."""
import logging
import os
from io import StringIO
from py_mel_logging import PythonLogger
from Python.Logging import DotNetPythonLogger

from clr_loader import get_coreclr
test_path = os.getcwd()
rt = get_coreclr(test_path + r"/../config.json")
from pythonnet import set_runtime

set_runtime(rt)
import clr

clr.AddReference("System")
clr.AddReference(r"Microsoft.Extensions.Logging.Abstractions")

from System import Exception as DotNetException
from System import Func, String
from Microsoft.Extensions.Logging import EventId, LogLevel


def test_is_enabled_returns_false_for_disabled_level():
    # Setup
    pylogger = PythonLogger(logging.WARN, logging.NullHandler())
    sut = DotNetPythonLogger(pylogger)

    # SUT
    result: bool = sut.IsEnabled(LogLevel.Debug)

    # Verification
    assert result is False


def test_is_enabled_returns_true_for_enabled_level():
    # Setup
    pylogger = PythonLogger(logging.DEBUG, logging.NullHandler())
    sut = DotNetPythonLogger(pylogger)

    # SUT
    result: bool = sut.IsEnabled(LogLevel.Debug)

    # Verification
    assert result is True


def test_log_with_no_formatter_or_exception():
    # Setup
    result = StringIO()
    handler = logging.StreamHandler(result)
    handler.setLevel(logging.DEBUG)

    pylogger = PythonLogger(logging.DEBUG, handler)
    sut = DotNetPythonLogger(pylogger)

    # SUT
    sut.Log[str](LogLevel.Warning, EventId(0), "Eyy", None, None)

    # Verification
    handler.flush()
    assert result.getvalue() == "[0] : Eyy\n"


def test_log_with_exception_and_no_formatter():
    # Setup
    result = StringIO()
    handler = logging.StreamHandler(result)
    handler.setLevel(logging.DEBUG)

    pylogger = PythonLogger(logging.DEBUG, handler)
    sut = DotNetPythonLogger(pylogger)

    ex = DotNetException("bruh")

    # SUT
    sut.Log[str](LogLevel.Warning, EventId(0), "Eyy", ex, None)

    # Verification
    handler.flush()
    assert result.getvalue() == "[0] : Eyy\nException: bruh\n"


def test_log_with_formatter():
    # Setup
    result = StringIO()
    handler = logging.StreamHandler(result)
    handler.setLevel(logging.DEBUG)

    pylogger = PythonLogger(logging.DEBUG, handler)
    sut = DotNetPythonLogger(pylogger)

    ex = DotNetException("bruh")

    def pyformatter(state, exception):
        return "☯" + state + " - " + exception.Message

    formatter = Func[String, DotNetException, String](pyformatter)

    # SUT
    sut.Log[str](LogLevel.Warning, EventId(0), "Eyy", ex, formatter)

    # Verification
    handler.flush()
    assert result.getvalue() == "☯[0] : Eyy - bruh\n"
