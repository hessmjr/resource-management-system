from flask import Blueprint
from services.add_incident_service import AddIncidentService

add_incident_bp = Blueprint('add_incident', __name__)


@add_incident_bp.route('/', methods=['GET', 'POST'])
def index():
    service = AddIncidentService()
    return service.handle_add_incident_request()
