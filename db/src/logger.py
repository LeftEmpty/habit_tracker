import logging

def setup_logger() -> logging.Logger:
    logger = logging.getLogger('logger')
    handler = logging.FileHandler('db_logs.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

logger: logging.Logger = setup_logger()