import logging
import sys
from collections import defaultdict

message_counts = defaultdict(int)

class TerminateOnExcessiveLogs(logging.Handler):
    def __init__(self, threshold = 10):
        super().__init__()
        self.threshold = threshold
    
    def emit(self, record):
        msg = self.format(record)
        message_counts[msg] += 1
        if message_counts[msg] >= self.threshold:
            print(f"Infinite loop {msg} ")
            sys.exit(1)

def setup_logger(name: str, log_file: str = "app.log" ):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(module)s - %(lineno)s - %(levelname)s - %(message)s'
    )
    
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    """
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    terminate_handler = TerminateOnExcessiveLogs(threshold = 10)
    terminate_handler.setLevel(logging.DEBUG) 
    terminate_handler.setFormatter(formatter)
    logger.addHandler(terminate_handler)
    
    return logger