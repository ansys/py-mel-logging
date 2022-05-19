"""Implementation of PythonLoggerProvider."""
import clr  # type: ignore

clr.AddReference(r"dlls\netstandard2.0\Microsoft.Extensions.Logging.Abstractions")
from Microsoft.Extensions.Logging import ILogger  # type: ignore


class PythonLoggerProvider:
    """TODO."""

    def create_logger(self, category_name: str) -> ILogger:
        """
        TODO.

        Parameters
        ----------
        category_name

        Returns
        -------
        TODO
        """
        raise NotImplementedError
