from flask import Blueprint
from services.search_resources_service import SearchResourcesService

search_resources_bp = Blueprint('search_resources', __name__)


@search_resources_bp.route('/', methods=['GET', 'POST'])
def index():
    service = SearchResourcesService()
    return service.handle_search_resources_request()


@search_resources_bp.route('/search-resources/request/', methods=['GET'])
def search_results_resource_request():
    service = SearchResourcesService()
    return service.handle_resource_request()


@search_resources_bp.route('/search-resources/repair/', methods=['GET'])
def search_results_resource_repair():
    service = SearchResourcesService()
    return service.handle_resource_repair()


@search_resources_bp.route('/search-resources/deploy/', methods=['GET'])
def search_results_resource_deploy():
    service = SearchResourcesService()
    return service.handle_resource_deploy()
