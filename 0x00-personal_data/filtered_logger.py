#!/usr/bin/env python3
"""
Regex-ing
"""


import re
from typing import List


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