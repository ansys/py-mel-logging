using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using Microsoft.Extensions.Logging;

namespace Python.Logging
{
   /// <summary>
   /// Extensions for registering Python logging in a dependency injection framework.
   /// </summary>
   public static class PythonLoggerExtensions
   {
      /// <summary>
      /// Call this method during app configuration to register a provider into the dependency injection framework.
      /// </summary>
      /// <param name="serviceCollection">The IServiceCollection to setup.</param>
      /// <param name="provider">The PythonLoggerProvider to setup.</param>
      public static void ConfigureServiceCollection(IServiceCollection serviceCollection, PythonLoggerProvider provider)
      {
         serviceCollection.AddLogging((builder) => builder.AddPythonLogger(provider));
      }

      /// <summary>
      /// Extension method to add a PythonLoggerProvider to a service collection.
      /// </summary>
      /// <param name="builder">The ILoggingBuilder provided during IServiceCollection.AddLogging.</param>
      /// <param name="provider">The PythonLoggerProvider to register as a singleton.</param>
      /// <returns></returns>
      public static ILoggingBuilder AddPythonLogger(this ILoggingBuilder builder, PythonLoggerProvider provider)
      {
         builder.Services.TryAddEnumerable(ServiceDescriptor.Singleton<ILoggerProvider, PythonLoggerProvider>((a) => provider));
         return builder;
      }
   }
}

