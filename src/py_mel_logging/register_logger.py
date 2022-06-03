def register_logger(
        log_level: int, log_handler: logging.Handler,
        service_collection: Optional[msDI.ServiceCollection] = None
) -> msDI.ServiceCollection:
    """
    Register the Python logging system into a .Net DependencyInjection \
    ServiceCollection.

    Parameters
    ----------
    log_level :
        Initial log level for new logger objects, the minimum Python log
        level to issue log messages for.
    log_handler :
        Handler for dispatching messages to the correct location.
    service_collection :
        Optional .Net ServiceCollection to add to.  If not given, will
        allocation a new ServiceCollection.

    Returns
    -------
    ServiceCollection given or allocated, with the Python logger having
    been added.
    """
    return