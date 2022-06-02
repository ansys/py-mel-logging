def load_dotnet_python_logging() -> None:
    """Add the Dot-Net PythonLogging assembly."""
    import os
    import sys
    import clr  # type: ignore

    sys.path.append(os.path.join(os.path.dirname(__file__), "dlls/netstandard2.0"))
    clr.AddReference(r"PythonLogging")
