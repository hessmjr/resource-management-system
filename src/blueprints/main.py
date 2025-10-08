from typing import Dict, Any
from flask import Blueprint, render_template, session, request

from database import get_db
from routes.resource_status import resource_status_route, update_status_route
from routes.add_resource import add_resource_route
from routes.resource_report import resource_report_route
from routes.search_resources import search_resources_route
from routes.add_incident import add_incident_route
from routes.search_results import user_request, owner_deploy, owner_repair

main_bp = Blueprint('main', __name__)


@main_bp.route('/menu')
def menu() -> str:
    """
    Handler for menu page
    :return: rendered template for url
    """
    # try to get current session user
    username = session.get('username')

    if not username:
        return render_template("menu.html", details={})

    # get user details using parameterized query
    db = get_db()
    cursor = db.cursor()
    cursor.execute(_get_user_details_query(), (username,))

    # Get column names from cursor description
    column_names = [desc[0] for desc in cursor.description]
    user_details = cursor.fetchall()
    cursor.close()

    # ensure there are user details
    details: Dict[str, Any] = {}
    if user_details and len(user_details) > 0:
        user_row = user_details[0]

        # remove None values from the query
        for value, column_name in zip(user_row, column_names):
            if value is not None:
                details[column_name] = value

    return render_template("menu.html", details=details)


def _get_user_details_query() -> str:
    """
    Creates SQL for getting user details using parameterized query
    :return: SQL query string with parameter placeholder
    """
    return """
        SELECT
            user.name, company.headquarters, government_agency.jurisdiction,
            municipality.population_size, individual.job_title,
            individual.hired_date
        FROM user
        LEFT JOIN company
            ON company.username = user.username
        LEFT JOIN government_agency
            ON government_agency.username = user.username
        LEFT JOIN municipality
            ON municipality.username = user.username
        LEFT JOIN individual
            ON individual.username = user.username
        WHERE user.username = %s
    """


# Resource Management Routes
@main_bp.route('/add-resource', methods=['GET', 'POST'])
def add_resource():
    return add_resource_route()


@main_bp.route('/add-incident', methods=['GET', 'POST'])
def add_incident():
    return add_incident_route()


@main_bp.route('/search-resources', methods=['GET', 'POST'])
def search_resources():
    return search_resources_route()


@main_bp.route('/search-resources/request/', methods=['GET'])
def search_results_resource_request():
    resource_id = request.args.get('resource-id')
    incident_id = request.args.get('incident-id')
    return user_request(inc_id=incident_id, res_id=resource_id)


@main_bp.route('/search-resources/repair/', methods=['GET'])
def search_results_resource_repair():
    resource_id = request.args.get('resource-id')
    return owner_repair(res_id=resource_id)


@main_bp.route('/search-resources/deploy/', methods=['GET'])
def search_results_resource_deploy():
    resource_id = request.args.get('resource-id')
    incident_id = request.args.get('incident-id')
    return owner_deploy(inc_id=incident_id, res_id=resource_id)


@main_bp.route('/resource-status', methods=['GET'])
def resource_status():
    return resource_status_route()


@main_bp.route('/resource-status/deploy', methods=['GET'])
def deploy_resource():
    return update_status_route()


@main_bp.route('/resource-status/return', methods=['GET'])
def return_resource():
    return update_status_route()


@main_bp.route('/resource-status/reject', methods=['GET'])
def reject_resource():
    return update_status_route()


@main_bp.route('/resource-status/request/cancel', methods=['GET'])
def cancel_resource_request():
    return update_status_route()


@main_bp.route('/resource-status/repair/cancel', methods=['GET'])
def cancel_resource_repair():
    return update_status_route()


@main_bp.route('/resource-report', methods=['GET'])
def resource_report():
    return resource_report_route()