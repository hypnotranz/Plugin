# logger_config.py

import logging
from pythonjsonlogger import jsonlogger
from uuid import uuid4

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['uuid'] = str(uuid4())  # add a unique id for each log record

def configure_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    logHandler = logging.StreamHandler()
    formatter = CustomJsonFormatter()
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    return logger
