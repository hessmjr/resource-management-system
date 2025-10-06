"""Configuration and database connection management for ERMS."""

import os
import json
from flask import g
from dbConnect import DBConnect


class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DATABASE_CONFIG_FILE = os.environ.get('DATABASE_CONFIG_FILE') or 'credentials.json'


def get_db_config():
    """Get database configuration from credentials file."""
    try:
        with open(Config.DATABASE_CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Database configuration file {Config.DATABASE_CONFIG_FILE} not found")


def connect_db():
    """Connect to database using configuration."""
    return DBConnect(Config.DATABASE_CONFIG_FILE)


def get_db():
    """Get database connection for current application context."""
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = connect_db()
    return g.mysql_db


def query_db(query, params=None):
    """Execute a SELECT query and return results."""
    if not query or len(query.strip()) < 1:
        return None
    
    db = get_db()
    if params:
        db.cursor.execute(query, params)
    else:
        db.cursor.execute(query)
    return db.cursor.fetchall()


def execute_db(query, params=None):
    """Execute a query and commit changes."""
    db = get_db()
    if params:
        db.cursor.execute(query, params)
    else:
        db.cursor.execute(query)
    db.commit()
    return db.cursor.lastrowid if db.cursor.lastrowid else None


def get_column_names(cursor):
    """Get column names from cursor description."""
    return [desc[0] for desc in cursor.description] if cursor.description else []