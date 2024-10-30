import logging

def setup_logger():
    """
    Sets up the logger for the hotel management system.

    This function configures the logging system to log messages to a specified log file.
    It defines the log format, log level, and file mode. It also sets the log level for
    the Snowflake connector to WARNING to reduce verbosity.

    Returns:
        logging.Logger: The configured logger instance.
    """
    logging.basicConfig(
        filename='hotel_system.log',
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logging.getLogger('snowflake.connector').setLevel(logging.WARNING)
    return logging.getLogger()