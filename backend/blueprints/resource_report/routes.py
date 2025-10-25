from flask import Blueprint
from services.resource_report_service import ResourceReportService

resource_report_bp = Blueprint("resource_report", __name__)


@resource_report_bp.route("/")
def index():
    service = ResourceReportService()
    return service.handle_resource_report_request()
