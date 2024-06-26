#!/usr/bin/env python3
"""
Regex-ing
"""


import re
from typing import List
import logging
import csv
import os
import mysql.connector
from mysql.connector import Error
# from filtered_logger import filter_datum
# from filtered_logger import filter_datum, RedactingFormatter, get_db
#from filtered_logger import get_db



class RedactingFormatter(logging.Formatter):
    """ 
    Redacting Formatter class
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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the MySQL database.

    The database credentials are obtained from environment variables:
    - PERSONAL_DATA_DB_USERNAME: username for the database (default: "root")
    - PERSONAL_DATA_DB_PASSWORD: password for the database (default: "")
    - PERSONAL_DATA_DB_HOST: host for the database (default: "localhost")
    - PERSONAL_DATA_DB_NAME: name of the database
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    try:
        conn = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=db_name
        )
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        raise


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

def main() -> None:
    """
    Retrieves all rows in the users table from the database and displays each row under a filtered format.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False

    try:
        conn = get_db()
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            for row in rows:
                message = "; ".join([f"{key}={value}" for key, value in row.items()])
                logger.info(message)
            cursor.close()
    except Error as e:
        logger.error(f"Error: {e}")
