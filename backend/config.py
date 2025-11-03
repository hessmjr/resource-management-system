import os
from typing import Any


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # Database configuration
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = int(os.environ.get("DB_PORT", "3306"))
    DB_NAME = os.environ.get("DB_NAME", "rms_db")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")

    # Flask configuration
    DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() in ("true", "1", "t")
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    # Use consistent secret key in development to persist sessions across restarts
    # Override with SECRET_KEY environment variable if needed
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")


class TestingConfig(Config):
    TESTING = True
    DEBUG = True

    DB_HOST = "localhost"
    DB_PORT = 23306
    DB_NAME = "rms_test_db"


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
