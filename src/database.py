from dbConnect import DBConnect
from flask import g


def connect_db():
    """
    Connects to database
    :return: DBConnect database
    """
    return DBConnect('credentials.json')


def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    :return: database connection
    """
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = connect_db()
    return g.mysql_db


def query_db(query):
    """
    Queries the database with given SQL string
    :return: result of query
    """
    # do precheck to make sure something there to query
    if query is None or len(query) < 1:
        return None

    # get the database and execute the query
    db = get_db()
    db.cursor.execute(query)
    return db.cursor.fetchall()


def commit_db(query):
    """
    Commits the new, unsaved changes
    :return:
    """
    db = get_db()
    db.cursor.execute(query)
    db.commit()
