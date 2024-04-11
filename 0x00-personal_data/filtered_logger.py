#!/usr/bin/env python3
"""
Regex-ing
"""


import re
from typing import List
import logging
import csv
# from filtered_logger import filter_datum


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"


    def __init__(self, fields: List[str]):
        """
        init function
        """
        super().__init__(self.FORMAT)
        self.fields = fields


    def format(self, record: logging.LogRecord) -> str:
        """
        format function
        """
        record.message = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super().format(record)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object named "user_data" that logs up to logging.INFO level.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger

    
def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Arguments:
    fields: A list of strings representing the fields to obfuscate.
    redaction: A string representing the redaction value to replace the fields with.
    message: A string representing the log line.
    separator: A string representing the character separating all fields in the log line.

    Returns:
    A string with specified fields obfuscated.
    """
    return re.sub(
        r'(?<=^|\b)(' + '|'.join(fields) + r')(?=\b|$)', 
        redaction, 
        message, 
        flags=re.IGNORECASE
    )

