from flask import Blueprint
from services.menu_service import MenuService

menu_bp = Blueprint('menu', __name__)


@menu_bp.route('/')
def index() -> str:
    service = MenuService()
    return service.get_menu_page()
