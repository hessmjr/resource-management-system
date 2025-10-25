import os

from blueprints.add_resource.routes import add_resource_bp
from blueprints.add_incident.routes import add_incident_bp
from blueprints.auth.routes import auth_bp
from blueprints.menu.routes import menu_bp
from blueprints.resource_report.routes import resource_report_bp
from blueprints.resource_status.routes import resource_status_bp
from blueprints.search_resources.routes import search_resources_bp
from config import config
from dotenv import load_dotenv
from flask import Flask, redirect, request, session, url_for

load_dotenv()


def create_app(config_name: str = 'default') -> Flask:
    app = Flask(__name__,
                template_folder='../frontend/templates',
                static_folder='../frontend/static')

    app.config.from_object(config[config_name])

    app.register_blueprint(add_resource_bp, url_prefix='/add-resource')
    app.register_blueprint(add_incident_bp, url_prefix='/add-incident')
    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp, url_prefix='/menu')
    app.register_blueprint(resource_report_bp, url_prefix='/resource-report')
    app.register_blueprint(resource_status_bp, url_prefix='/resource-status')
    app.register_blueprint(search_resources_bp, url_prefix='/search-resources')

    @app.before_request
    def before_request():
        if (request.endpoint and
            (request.endpoint.startswith('auth.') or
             request.endpoint == 'static' or
             (request.url and 'static' in request.url))):
            return None

        if 'username' not in session and 'name' not in session:
            return redirect(url_for('auth.login'))

        return None

    return app


config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)  # noqa: S104
