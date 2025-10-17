import os
from typing import Optional

from flask import Flask, session, redirect, url_for, request
from dotenv import load_dotenv

from blueprints.auth import auth_bp
from blueprints.main import main_bp
from config import config

# Load environment variables
load_dotenv()

def create_app(config_name: str = 'default') -> Flask:
    """Application factory pattern."""
    app = Flask(__name__,
                template_folder='../frontend/templates',
                static_folder='../frontend/static')

    # Load configuration
    app.config.from_object(config[config_name])

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app

# Create app instance
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

# Authentication check for all routes
@app.before_request
def before_request() -> Optional[redirect]:
    """
    Before any request check if the user is already logged in.
    """
    # Allow access to auth routes and static files
    if (request.endpoint and
        (request.endpoint.startswith('auth.') or
         request.endpoint == 'static' or
         (request.url and 'static' in request.url))):
        return None

    # if user is not already logged in redirect to login pages
    if 'username' not in session and 'name' not in session:
        return redirect(url_for('auth.login'))

    return None


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)
