import logging

# stacklevel=2 attributes each record to the caller's file and line, not this module.


def get_logger(name: str):
    logger = logging.getLogger(name)
    return logger


def log_step(logger, message: str):
    logger.info(f"[STEP] {message}", stacklevel=2)


def log_data(logger, data: dict):
    logger.info(f"[DATA] {data}", stacklevel=2)


def log_debug(logger, message: str):
    logger.debug(message, stacklevel=2)


def log_warning(logger, message: str):
    logger.warning(message, stacklevel=2)


def log_error(logger, message: str):
    logger.error(message, stacklevel=2)
