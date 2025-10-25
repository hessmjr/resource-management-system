"""
Test configuration and shared fixtures.
Assumes Docker services are already running.
"""

import pytest
from app import create_app
from database import commit_db, get_db


@pytest.fixture
def app():
    """Create Flask app with isolated test database."""
    app = create_app("testing")
    app.config["TESTING"] = True
    # Use separate test database
    app.config["DB_NAME"] = "rms_test_db"
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def setup_test_db():
    """Set up isolated test database with schema and reference data."""
    import os
    import subprocess

    # Create test database
    subprocess.run([
        "docker", "exec", "rms-mysql", "mysql", "-u", "root", "-ppassword",
        "-e", "CREATE DATABASE IF NOT EXISTS rms_test_db;"
    ], check=True)

    # Run schema creation script on test database
    schema_path = os.path.join(os.path.dirname(__file__), "..", "backend", "sql", "creation_script.sql")
    subprocess.run([
        "docker", "exec", "-i", "rms-mysql", "mysql", "-u", "root", "-ppassword", "rms_test_db"
    ], stdin=open(schema_path), check=True)

    # Run reference data insertion script on test database
    insert_path = os.path.join(os.path.dirname(__file__), "..", "backend", "sql", "insert_statements_script.sql")
    subprocess.run([
        "docker", "exec", "-i", "rms-mysql", "mysql", "-u", "root", "-ppassword", "rms_test_db"
    ], stdin=open(insert_path), check=True)

    yield

    # Clean up test database after all tests
    subprocess.run([
        "docker", "exec", "rms-mysql", "mysql", "-u", "root", "-ppassword",
        "-e", "DROP DATABASE IF EXISTS rms_test_db;"
    ], check=True)


@pytest.fixture
def clean_db(app, setup_test_db):
    """Clean user-generated data before each test."""
    with app.app_context():
        # Clean user-generated data in dependency order
        # Keep reference data: esf, cost_time_period
        commit_db("DELETE FROM resource_request_status")
        commit_db("DELETE FROM resource_esf")
        commit_db("DELETE FROM capability")
        commit_db("DELETE FROM resource")
        commit_db("DELETE FROM incident")
        commit_db("DELETE FROM municipality")
        commit_db("DELETE FROM individual")
        commit_db("DELETE FROM government_agency")
        commit_db("DELETE FROM company")
        commit_db("DELETE FROM user")
        yield


@pytest.fixture
def db_session(app):
    with app.app_context():
        return get_db()
