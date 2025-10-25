from flask import Blueprint
from services.resource_status_service import ResourceStatusService

resource_status_bp = Blueprint("resource_status", __name__)


@resource_status_bp.route("/")
def index(error=None):
    service = ResourceStatusService()
    return service.get_resource_status_page(error)


@resource_status_bp.route("/resource-status/deploy", methods=["GET"])
def deploy_resource():
    service = ResourceStatusService()
    return service.update_resource_status()


@resource_status_bp.route("/resource-status/return", methods=["GET"])
def return_resource():
    service = ResourceStatusService()
    return service.update_resource_status()


@resource_status_bp.route("/resource-status/reject", methods=["GET"])
def reject_resource():
    service = ResourceStatusService()
    return service.update_resource_status()


@resource_status_bp.route("/resource-status/request/cancel", methods=["GET"])
def cancel_resource_request():
    service = ResourceStatusService()
    return service.update_resource_status()


@resource_status_bp.route("/resource-status/repair/cancel", methods=["GET"])
def cancel_resource_repair():
    service = ResourceStatusService()
    return service.update_resource_status()
