from typing import Dict, Any
from flask import render_template, session

from database import get_db, query_db


def menu_route() -> str:
    """
    Handler for menu page
    :return: rendered template for url
    """
    # try to get current session user
    username = session.get('username')

    if not username:
        return render_template("menu.html", details={})

    # get user details using parameterized query
    user_details = query_db(_get_user_details_query(), (username,))
    db = get_db()

    # ensure there are user details
    details: Dict[str, Any] = {}
    if user_details and len(user_details) > 0:
        user_row = user_details[0]

        # Get column names from cursor
        cursor = db.cursor()
        cursor.execute(_get_user_details_query(), (username,))
        column_names = [desc[0] for desc in cursor.description]
        cursor.close()

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
