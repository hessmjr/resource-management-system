from flask import Blueprint
from services.resource_service import ResourceService

add_resource_bp = Blueprint('add_resource', __name__)


@add_resource_bp.route('/add-resource', methods=['GET', 'POST'])
def add_resource(error=None):
    service = ResourceService()
    return service.handle_add_resource_request(error)
