from typing import Any

from dal.menu_dal import MenuDAL
from flask import render_template, session


class MenuService:
    def __init__(self):
        self.dal = MenuDAL()

    def get_menu_page(self) -> str:
        username = session.get('username')

        if not username:
            return render_template("menu.html", details={})

        user_details = self.dal.get_user_details(username)

        details: dict[str, Any] = {}
        if user_details and len(user_details) > 0:
            user_row = user_details[0]
            column_names = self.dal.get_user_details_columns()

            for value, column_name in zip(user_row, column_names, strict=True):
                if value is not None:
                    details[column_name] = value

        return render_template("menu.html", details=details)
