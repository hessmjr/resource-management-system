from datetime import datetime
from re import compile, match
from string import Template
from uuid import uuid4

from flask import *

from src.database import commit_db


def add_incident_route(error=None):
    """
    Adds incident to system; return template
    :param error - message ot pass to user if any specified
    """
    # get owner and create ID
    username = session.get('username')
    incident_id = int(uuid4().int / 10.0**29)

    # build new incident form for user
    if request.method == 'GET':

        # create new incident template
        return render_template('add_incident.html', incident_id=incident_id,
                               error=error)

    # input from the user's form
    elif request.method == 'POST':

        # if user saving form then insert into database
        if 'Save' in request.form:
            error = add_new_incident(username)

        # if user canceled or there is no errors return to menu
        if 'Cancel' in request.form or not error:
            flash('Resource successfully created.')
            return redirect(url_for('menu'))

        # if user has an error then save id from the form
        if 'incident_id' in request.form:
            incident_id = request.form['incident_id']

        # return template with error message and status
        return render_template('add_incident.html', incident_id=incident_id,
                               error=error), 400

    # invalid user request, abort
    return abort(405)


def add_new_incident(username):
    """
    Helper method for creating a new incident
    :param username: owner's username
    :return: error message if any
    """
    # check input values exist
    if 'incident_id' not in request.form or 'lat' not in request.form or \
            'long' not in request.form or 'date' not in request.form:
        return "Missing parameter to add incident"

    # get all input values
    incident_id = request.form['incident_id']
    description = request.form['description']
    incident_date = request.form['date']
    lat = request.form['lat']
    lng = request.form['long']

    # validate lat and long
    lat_regex = compile('^-?([1-8]?[0-9]|[1-9]0)\.\d{1,6}$')
    long_regex = compile('^-?(1[0-8][0-9]|[0-9]{1,2})\.\d{1,6}$')

    if not match(long_regex, lng) or not match(lat_regex, lat):
        return "Invalid latitude/longitude format"

    # validate incident date
    try:
        datetime.strptime(incident_date, '%Y-%m-%d')
    except ValueError:
        return "Invalid incident date format. Please input YYYY-MM-DD"

    # SQL template
    t = Template("""
        INSERT INTO incident
        VALUES ('$incident_id', '$username', '$description','$latitude',
            '$longitude', '$incident_date')
    """)

    # substitue user values
    query = t.safe_substitute({'incident_id': incident_id, 'username': username,
                               'description': description, 'latitude': lat,
                               'longitude': lng, 'incident_date': incident_date})
    print query
    # commit and return to user
    commit_db(query)
    return None
