import logging

def setup_logger(name: str, level = logging.info):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    formatter = logging.Formatter
    ('%(asctime)s - %(module)s - %(lineno)s - %(levelname)s - %(message)s')
    
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger