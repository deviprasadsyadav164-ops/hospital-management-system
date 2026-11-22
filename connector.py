import os

import mysql.connector


def get_connection(password=None):
    """Connect to the configured hospital database without storing credentials."""
    password = password or os.environ.get("HOSPITAL_DB_PASSWORD")
    if not password:
        raise ValueError(
            "Set HOSPITAL_DB_PASSWORD or enter a password in the app prompt."
        )
    return mysql.connector.connect(
        host=os.environ.get("HOSPITAL_DB_HOST", "localhost"),
        user=os.environ.get("HOSPITAL_DB_USER", "root"),
        password=password,
        database=os.environ.get("HOSPITAL_DB_NAME", "hospitalmanagementd"),
    )