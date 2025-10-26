from typing import Any

import mysql.connector
from config import Config
from flask import current_app, g


def connect_db() -> mysql.connector.MySQLConnection:
    """
    Connects to database using configuration.
    :return: MySQL database connection
    """
    try:
        # Use Flask app's configuration directly
        config = {
            "host": current_app.config["DB_HOST"],
            "port": current_app.config["DB_PORT"],
            "user": current_app.config["DB_USER"],
            "password": current_app.config["DB_PASSWORD"],
            "database": current_app.config["DB_NAME"],
            "autocommit": False,
        }
        return mysql.connector.connect(**config)
    except Exception as e:
        current_app.logger.error(f"Database connection error: {e}")
        raise


def get_db() -> mysql.connector.MySQLConnection:
    """
    Opens a new database connection if there is none yet for the
    current application context.
    :return: database connection
    """
    if not hasattr(g, "mysql_db"):
        g.mysql_db = connect_db()
    return g.mysql_db


def query_db(query: str, params: tuple | None = None) -> list[tuple[Any, ...]] | None:
    """
    Queries the database with given SQL string and parameters.
    :param query: SQL query string
    :param params: Query parameters for prepared statements
    :return: result of query
    """
    # do precheck to make sure something there to query
    if not query or len(query.strip()) < 1:
        return None

    try:
        # get the database and execute the query
        db = get_db()
        cursor = db.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print(f"Query error: {e}")
        raise


def commit_db(query: str, params: tuple | None = None) -> None:
    """
    Commits the new, unsaved changes to the database.
    :param query: SQL query string
    :param params: Query parameters for prepared statements
    """
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(query, params)
        db.commit()
        cursor.close()
    except Exception as e:
        print(f"Commit error: {e}")
        db.rollback()
        raise
