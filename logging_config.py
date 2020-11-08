import logging

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —"
    "%(funcName)s:%(lineno)d — %(message)s",
    "%Y-%m-%d %H:%M:%S"
    )

LOG_FILE = "log.txt"


def get_file_handler():
    file_handler = logging.FileHandler(
        LOG_FILE,
        mode="w",
        encoding="utf-8",
        )
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(logging.DEBUG)
    return file_handler


def get_logger(*, logger_name):
    """Get logger with prepared handlers."""
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.DEBUG)

    logger.addHandler(get_file_handler())
    logger.propagate = False

    return logger
