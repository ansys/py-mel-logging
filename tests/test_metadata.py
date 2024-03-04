from py_mel_logging import __version__
from System.Runtime.InteropServices import RuntimeInformation


def test_pkg_version():
    assert __version__ == "0.2.dev1"


def test_framework_description():
    print()
    fd = RuntimeInformation.FrameworkDescription
    print(f"Framework Description: {fd}")
