from string import Template

from flask import render_template, session

from src.database import get_db, query_db


def menu_route(message=None):
    """
    Handler for menu page
    :return: rendered template for url
    """
    # try to get current session user
    username = session.get('username')

    # get user details
    user_details = query_db(get_user_details_query(username))
    db = get_db()

    # ensure there are user details
    details = {}
    if len(user_details) > 0:
        user_details = user_details[0]

        # remove None values from the query
        for a, b in zip(user_details, db.cursor.description):
            if a is not None:
                details[b[0]] = a

    return render_template("menu.html", details=details)


def get_user_details_query(username):
    """
    Creates SQL for getting user details
    """
    t = Template("""
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
        WHERE user.username = '$username'
    """)

    return t.safe_substitute({'username': username})
