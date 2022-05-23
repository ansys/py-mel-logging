using Microsoft.Extensions.Logging;
using Python.Runtime;
using System;
using System.Collections.Concurrent;

namespace Python.Logging
{
   /// <summary>
   /// Implementation of <see cref="Microsoft.Extensions.Logging.ILoggerProvider"/> that creates 
   /// <see cref="DotNetPythonLogger"/>s from a single python logger. Logging configuration should be done on the
   /// python side, by creating the appropriate handlers and formatters for the logger used.
   /// </summary>
   public class PythonLoggerProvider : ILoggerProvider
   {
      /// <summary>
      /// Function to ask the python side for a new python logger when creating a new .Net logger.
      /// </summary>
      private Func<PyObject> _createPyLoggerFunc = null;

      /// <summary>
      /// A cache of loggers by name to avoid multiple creation cost.
      /// </summary>
      private readonly ConcurrentDictionary<string, DotNetPythonLogger> _loggers = 
         new ConcurrentDictionary<string, DotNetPythonLogger>();

      /// <summary>
      /// Constructor.
      /// </summary>
      /// <param name="createPyLoggerFunc">Function to ask the python side for a new python logger when creating
      /// a new .Net logger.</param>
      public PythonLoggerProvider(Func<PyObject> createPyLoggerFunc)
      {
         if (!PythonEngine.IsInitialized)
         {
            PythonEngine.Initialize();
         }
         _createPyLoggerFunc = createPyLoggerFunc;
      }

      /// <inheritdoc />
      public ILogger CreateLogger(string categoryName)
      {
         return _loggers.GetOrAdd(categoryName, _createLogger);
      }

      /// <summary>
      /// Actual implementation of creating a logger, only used if it is not already created.
      /// </summary>
      /// <param name="name">The name of the logger.</param>
      /// <returns>A new <see cref="DotNetPythonLogger"/>.</returns>
      private DotNetPythonLogger _createLogger(string name)
      {
         using (Py.GIL())
         {
            PyObject pyLogger = _createPyLoggerFunc();
            return new DotNetPythonLogger(pyLogger);
         }
      }

      /// <inheritdoc />
      public void Dispose()
      {
         GC.SuppressFinalize(this);
      }
   }
}

