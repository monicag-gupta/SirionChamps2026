import os

import mysql.connector

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
}

DB_NAME = os.environ.get("DB_NAME", "training_db")


def get_connection(with_database=True):
    config = dict(DB_CONFIG)
    if with_database:
        config["database"] = DB_NAME
    return mysql.connector.connect(**config)
