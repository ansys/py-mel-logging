using Microsoft.Extensions.Logging;
using Python.Runtime;
using System;

namespace Python.Logging
{
   /// <summary>
   /// Lightweight implementation of <see cref="Microsoft.Extensions.Logging.ILogger"/> that calls through to a
   /// Python object.
   /// </summary>
   public class DotNetPythonLogger : ILogger
   {
      /// <summary>
      /// The Python object used for logging.
      /// Expected to be a py_mle_logging.PythonLogger, but can be any python object that has the required methods;
      /// see method documentation for details.
      /// </summary>
      private PyObject _logger;

      /// <summary>
      /// Constructor.
      /// </summary>
      /// <param name="logger">The Python logger to use for logging.</param>
      public DotNetPythonLogger(PyObject logger)
      {
         if (!PythonEngine.IsInitialized)
         {
            PythonEngine.Initialize();
         }
         _logger = logger;
      }

      /// <inheritdoc/>
      /// <remarks>
      /// Currently not supported for Python loggers.
      /// </remarks>
      public IDisposable BeginScope<TState>(TState state) => default;

      /// <inheritdoc/>
      /// <remarks>
      /// Calls through to 'is_enabled' method on the Python object.
      /// </remarks>
      public bool IsEnabled(LogLevel logLevel)
      {
         using (Py.GIL())
         {
            return (bool)_logger.InvokeMethod("is_enabled", logLevel.ToPython()).AsManagedObject(typeof(bool));
         }
      }

      /// <inheritdoc/>
      /// <remarks>
      /// Calls through to 'log' method on the Python object.
      /// </remarks>
      public void Log<TState>(LogLevel logLevel, EventId eventId, TState state, Exception exception, Func<TState, Exception, string> formatter)
      {
         using (Py.GIL())
         {
            var pyargs = new PyObject[]
            {
               logLevel.ToPython(),
               eventId.ToPython(),
               state.ToString().ToPython(),
               exception.ToPython(),
               formatter.ToPython()
            };
            _logger.InvokeMethod("log", pyargs);
         }
      }
   }
}

