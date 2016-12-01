import os.path
import sys

from flask import Flask, session, redirect, url_for, request

# necessary to ensure application specific modules are found
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from routes.resource_status import resource_status_route
from routes.login import index_route
from routes.add_resource import add_resource_route
from routes.menu import menu_route
from routes.resource_report import resource_report_route
from routes.search_resources import search_resources_route
from routes.add_incident import add_incident_route
from routes.search_results import user_request, owner_deploy, owner_repair

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ###########################
# Setup all route handling
# ###########################


@app.before_request
def before_request():
    """
    Before any request check if the user is already logged in.
    """
    if request.endpoint == 'login' or 'static' in request.url:
        return

    # if user is not already logged in redirect to login pages
    if 'username' not in session and 'name' not in session:
        return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    return index_route()


@app.route('/menu', methods=['GET'])
def menu():
    return menu_route()


@app.route('/add-resource', methods=['GET', 'POST'])
def add_resource():
    return add_resource_route()


@app.route('/add-incident', methods=['GET', 'POST'])
def add_incident():
    return add_incident_route()


@app.route('/search-resources', methods=['GET', 'POST'])
def search_resources():
    return search_resources_route()


@app.route('/search-resources/request/', methods=['GET'])
def search_results_resource_request():

    resource_id = request.args.get('resource-id')
    incident_id = request.args.get('incident-id')

    return user_request(inc_id=incident_id, res_id=resource_id )


@app.route('/search-resources/repair/', methods=['GET'])
def search_results_resource_repair():

    resource_id = request.args.get('resource-id')

    return owner_repair(res_id=resource_id)


@app.route('/search-resources/deploy/', methods=['GET'])
def search_results_resource_deploy():

    resource_id = request.args.get('resource-id')
    incident_id = request.args.get('incident-id')

    return owner_deploy(inc_id=incident_id, res_id=resource_id)


@app.route('/resource-status', methods=['GET'])
def resource_status():
    return resource_status_route()


@app.route('/resource-status/deploy', methods=['GET'])
def deploy_resource():
    return resource_status_route()


@app.route('/resource-status/return', methods=['GET'])
def return_resource():
    return resource_status_route()


@app.route('/resource-status/reject', methods=['GET'])
def reject_resource():
    return resource_status_route()


@app.route('/resource-status/request/cancel', methods=['GET'])
def cancel_resource_request():
    return resource_status_route()


@app.route('/resource-status/repair/cancel', methods=['GET'])
def cancel_resource_repair():
    return resource_status_route()


@app.route('/resource-report', methods=['GET'])
def resource_report():
    return resource_report_route()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
