"""Implementation of PythonLoggerProvider."""
import clr

clr.AddReference("Microsoft.Extensions.Logging.Abstractions")
from Microsoft.Extensions.Logging import ILogger


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
