"""Emergency Resource Management System Backend Application."""

from flask import Flask
from .config import get_db_config


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.secret_key = 'your-secret-key-here'  # Should be from environment in production
    
    # Register blueprints
    from .routes import api, auth
    app.register_blueprint(auth.bp)
    app.register_blueprint(api.bp)
    
    return app