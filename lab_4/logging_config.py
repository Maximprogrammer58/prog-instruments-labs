import logging


def setup_logging() -> None:
    """ Configures the basic logging configuration.

    Sets the logging level to INFO and sets the message format.
    The messages will be output to the standard output stream.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
