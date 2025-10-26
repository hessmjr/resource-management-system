"""
Test configuration and shared fixtures.
Assumes Docker services are already running.
"""

import sys
from pathlib import Path

import pytest

backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Add tests directory to Python path for fixtures
tests_path = Path(__file__).parent.parent
sys.path.insert(0, str(tests_path))

from app import create_app
from database import commit_db, get_db
from flask import g


@pytest.fixture
def app():
    """Create Flask app with isolated test database."""
    app = create_app("testing")
    app.config["TESTING"] = True
    app.config["DB_NAME"] = "rms_test_db"
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def setup_test_db():
    """Set up isolated test database with minimal schema."""
    import subprocess
    import time

    try:
        # Drop and recreate test database
        subprocess.run([
            "docker", "exec", "rms-mysql", "mysql", "-u", "root", "-ppassword",
            "-e", "DROP DATABASE IF EXISTS rms_test_db;"
        ], check=True, timeout=10)

        subprocess.run([
            "docker", "exec", "rms-mysql", "mysql", "-u", "root", "-ppassword",
            "-e", "CREATE DATABASE rms_test_db;"
        ], check=True, timeout=10)

        # Copy schema from main database
        schema_dump = subprocess.run([
            "docker", "exec", "rms-mysql", "mysqldump", "-u", "root", "-ppassword",
            "--no-data", "rms_db"
        ], stdout=subprocess.PIPE, check=True, timeout=30)

        subprocess.run([
            "docker", "exec", "-i", "rms-mysql", "mysql", "-u", "root", "-ppassword", "rms_test_db"
        ], input=schema_dump.stdout, check=True, timeout=30)

        # Copy reference data (ESF, cost_time_period, and resource_request_status)
        reference_data_dump = subprocess.run([
            "docker", "exec", "rms-mysql", "mysqldump", "-u", "root", "-ppassword",
            "--no-create-info", "--where=1", "rms_db", "esf", "cost_time_period", "resource_request_status"
        ], stdout=subprocess.PIPE, check=True, timeout=30)

        subprocess.run([
            "docker", "exec", "-i", "rms-mysql", "mysql", "-u", "root", "-ppassword", "rms_test_db"
        ], input=reference_data_dump.stdout, check=True, timeout=30)

        # Disable strict SQL mode for test database
        subprocess.run([
            "docker", "exec", "rms-mysql", "mysql", "-u", "root", "-ppassword",
            "-e", "SET GLOBAL sql_mode = '';"
        ], check=True, timeout=10)

    except (subprocess.TimeoutExpired, Exception) as e:
        print(f"Database setup failed: {e}")
        print("Attempting minimal fallback...")
        # Fallback: just ensure test database exists
        try:
            subprocess.run([
                "docker", "exec", "rms-mysql", "mysql", "-u", "root", "-ppassword",
                "-e", "CREATE DATABASE IF NOT EXISTS rms_test_db;"
            ], check=True, timeout=10)
        except Exception as fallback_error:
            print(f"Minimal database creation failed: {fallback_error}")

    yield

    # Clean up test database after all tests
    try:
        subprocess.run([
            "docker", "exec", "rms-mysql", "mysql", "-u", "root", "-ppassword",
            "-e", "DROP DATABASE IF EXISTS rms_test_db;"
        ], check=True, timeout=10)
    except subprocess.TimeoutExpired:
        print("Database cleanup timed out")
    except Exception as e:
        print(f"Database cleanup failed: {e}")


@pytest.fixture
def clean_db(app, setup_test_db):
    """Clean user-generated data before each test."""
    with app.app_context():
        try:
            # Clean user-generated data in dependency order (children first)
            # Keep reference data: esf, cost_time_period, resource_request_status
            cleanup_queries = [
                "DELETE FROM resource_request",
                "DELETE FROM resource_repair",
                "DELETE FROM resource_esf",
                "DELETE FROM capability",
                "DELETE FROM resource",
                "DELETE FROM incident",
                "DELETE FROM municipality",
                "DELETE FROM individual",
                "DELETE FROM government_agency",
                "DELETE FROM company",
                "DELETE FROM user"
            ]

            # Execute cleanup queries with error handling
            for query in cleanup_queries:
                try:
                    commit_db(query)
                except Exception as e:
                    print(f"Warning: Failed to execute {query}: {e}")
                    # Continue with other cleanup queries even if one fails

            yield

        finally:
            # Ensure cleanup happens even if test fails
            try:
                # Force close any open database connections
                if hasattr(g, 'mysql_db'):
                    try:
                        g.mysql_db.close()
                    except:
                        pass
                    delattr(g, 'mysql_db')
            except Exception as e:
                print(f"Warning: Error during cleanup: {e}")


@pytest.fixture
def db_session(app):
    with app.app_context():
        return get_db()
