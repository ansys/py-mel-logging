PyAnsys Microsoft Extensions Logging
####################################
|pyansys| |python| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/badge/Python-%3E%3D3.10-blue
   :target: https://pypi.org/project/py-cam-client/
   :alt: Python

.. TODO: pypi and GH-CI badges

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code_style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

About
-----
This repository provides a Python module for using a Python logger with
the Microsoft.Extensions.Logging framework.

PLEASE NOTE: this project is still a work in progress. 


Project Overview
----------------
Intended for use with Python libraries that call into .Net code via
`pythonnet <https://github.com/pythonnet/pythonnet/>`_, this library
allows for easy registration of a Python logging Handler into the .Net
dependency injection framework.


Installation
------------
The ``py-mel-logging`` package currently supports Python 3.10 through
3.13 on Windows and Linux. This package is not currently available on
PyPI, but will be when it is ready for use.
At that time you can install ``py-mel-logging`` with:

.. code::

   pip install py-mel-logging

Alternatively, install the latest from `py-mel-logging GitHub
<https://github.com/pyansys/py-mel-logging>`_ via:

.. code::

   pip install git+https://github.com/pyansys/py-mel-logging.git

For a local "development" version, install with:

.. code::

   git clone https://github.com/pyansys/py-mel-logging.git
   cd py-mel-logging
   pip install poetry
   poetry install

This creates a new virtual environment, which can be activated with

.. code::

   poetry env activate


Documentation
-------------
TODO: link to the full sphinx documentation. `py-mel-logging <https://py-mel-logging.docs.pyansys.com/>`_
For building documentation, you can run the usual rules provided in the Sphinx Makefile, such as:

.. code::

    make -C doc/ html && your_browser_name doc/html/index.html

on Unix, or:

.. code::

    .\doc\make.bat html

on Windows. Make sure the required dependencies are installed with:

.. code::

    poetry install -E docs

Usage
-----
Use this library to register a logger in a .NET dependency injection
system with the following:

.. code:: python

   ... setup a Python logging handler ...
   ... setup .Net ...
   >>> from py_mel_logging import create_logger_provider
   >>> import Microsoft.Extensions.DependencyInjection as DependencyInjection
   >>> from Python.Logging import PythonLoggerExtensions
   >>> provider = create_logger_provider(logging.WARN, handler)
   >>> sc = DependencyInjection.ServiceCollection()
   >>> PythonLoggerExtensions.ConfigureServiceCollection(sc, provider)
   >>> sp = DependencyInjection.ServiceCollectionContainerBuilderExtensions.BuildServiceProvider(sc)
   ... use the ServiceProvider in your application setup ...


Testing
-------
Dependencies required for testing can be installed via:

.. code::

    poetry install -E test

The tests can then be run via pytest.


License
-------
py-pacz is licensed under the MIT license.
