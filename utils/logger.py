import logging

def get_logger(name: str):
    logger = logging.getLogger(name)
    return logger

def log_step(logger, message: str):
    logger.info(f"[STEP] {message}")

def log_data(logger, data: dict):
    logger.info(f"[DATA] {data}")

def log_debug(logger, message: str):
    logger.debug(f"[DEBUG] {message}")

def log_warning(logger, message: str):
    logger.warning(f"[WARNING] {message}")

def log_error(logger, message: str):
    logger.error(f"[ERROR] {message}")