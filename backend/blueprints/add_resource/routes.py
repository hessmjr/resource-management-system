from flask import Blueprint
from services.resource_service import ResourceService

add_resource_bp = Blueprint('add_resource', __name__)


@add_resource_bp.route('/', methods=['GET', 'POST'])
def index(error=None):
    service = ResourceService()
    return service.handle_add_resource_request(error)
