from typing import Any, List, Optional, Tuple
import mysql.connector
from flask import g, current_app

from config import Config


def connect_db() -> mysql.connector.MySQLConnection:
    """
    Connects to database using configuration.
    :return: MySQL database connection
    """
    try:
        config = Config.get_database_config()
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
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = connect_db()
    return g.mysql_db


def query_db(query: str, params: Optional[Tuple] = None) -> Optional[List[Tuple[Any, ...]]]:
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


def commit_db(query: str, params: Optional[Tuple] = None) -> None:
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
