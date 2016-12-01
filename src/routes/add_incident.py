from re import compile, match
from string import Template
from uuid import uuid4

from flask import render_template, request, session, redirect, url_for, abort

from src.database import commit_db


def add_incident_route(error=None):
    """
    Adds incident to system; return template
    """
    # get owner
    username = session.get('username')

    # build new incident form for user
    if request.method == 'GET':
        # create unique ID of incident
        incident_id = create_incident_id()
        return render_template('add_incident.html', incident_id=incident_id,
                               error=error)

    # input from the user's form
    elif request.method == 'POST':

        if 'Save' in request.form:
            error = add_inc(username)

        if 'Cancel' in request.form or not error:
            return redirect(url_for('menu'))

        incident_id = create_incident_id()
        if 'incident_id' in request.form:
            incident_id = request.form['incident_id']

        return render_template('add_incident.html', incident_id=incident_id,
                               error=error), 400
    return abort(405)


def create_incident_id():
    return int(uuid4().int >> 96)


def new_incident_sql(incident_id, username, desp, lat, lng, inc_date):
    """

    :param incident_id:
    :param username:
    :param desp:
    :param lat:
    :param lng:
    :param inc_date:
    :return:
    """

    t = Template("""
        INSERT INTO `emergency_response_system`.`incident`
        VALUES ('$incident_id', '$username', '$description','$latitude',
        '$longitude', '$incident_date')
    """)
    return t.safe_substitute({'incident_id': incident_id, 'username': username,
                              'description': desp, 'latitude': lat,
                              'longitude': lng, 'incident_date': inc_date})


def add_inc(username):
    # check input values exist
    if 'incident_id' not in request.form or 'lat' not in request.form or 'long' not in request.form \
            or 'date' not in request.form:
        return "Missing parameter to add incident"

    # get all input values
    incident_id = request.form['incident_id']
    description = request.form['description']
    incident_date = request.form['date']
    lat = request.form['lat']
    lng = request.form['long']

    # validate lat and long
    # lat_regex = compile('^-?([1-8]?[1-9]|[1-9]0)\.\d{1,6}$')
    # long_regex = compile('^-?(1[1-8][1-9]|[0-9]{1,2})\.\d{1,6}$')
    lat_regex = compile('^-?([1-8]?\d(\.\d+)?|90(\.0+)?)$')
    long_regex = compile('^-?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$')

    if not match(long_regex, lng) or not match(lat_regex, lat):
        return "Invalid latitude/longitude format"

    # validate incident date
    from datetime import datetime
    try:
        datetime.strptime(incident_date, "%m/%d/%Y")
    except ValueError:
        return "Invalid incident date format. Please input MM/DD/YYYY"

    # insert into db
    commit_db(new_incident_sql(incident_id, username, description, lat, lng, incident_date))
    return None
