from string import Template

from flask import render_template, request, redirect, url_for, session

from src.database import query_db


def search_resources_route(error=None):
    """
    Adds a new resource to the system
    :return: template after user decision
    """
    username = session.get('username')

    # get all ESF's
    esfs = query_db("SELECT * FROM esf")

    # get all incidents
    incidents = query_db(get_incidents_sql(username))

    # if user is requesting the page then get everything necessary
    if request.method == 'GET':
        return render_template('search_resources.html', esfs=esfs,
                               incidents=incidents, error=error)

    # if user is posting a new search
    elif request.method == 'POST':
        # if user cancels then return to menu
        if 'cancel' in request.form:
            return redirect(url_for('menu'))

        # set query params
        esf_id, keyword, distance, inc_id = "", "", "", ""
        incident = None

        # extract params
        if 'esf' in request.form:
            esf_id = request.form['esf']

        if 'keyword' in request.form:
            keyword = request.form['keyword']

        if 'distance' in request.form:
            distance = request.form['distance']

        if 'incident_id' in request.form:
            inc_id = request.form['incident_id']

        # check if distance value is valid
        if len(distance) > 0:
            if not unicode.isnumeric(distance):
                error = "Distance value must be positive number"
                return render_template('search_resources.html', esfs=esfs,
                                       incidents=incidents, error=error)

        # pick query based on params user passed
        # if keyword was entered and nothing else
        if len(keyword) > 0 and len(esf_id) < 1 and len(inc_id) < 1:
            results = query_db(keyword_sql(keyword))

        # if esf was given and nothing else
        elif len(keyword) < 1 and len(esf_id) > 0 and len(inc_id) < 1:
            results = query_db(esf_sql(esf_id))

        # if incident was given and nothing else
        elif len(keyword) < 1 and len(esf_id) < 1 and len(inc_id) > 0:
            incident = query_db(get_incident_sql(inc_id))[0]
            results = query_db(incident_sql(inc_id, distance))

        # if keyword and esf were given
        elif len(keyword) > 0 and len(esf_id) > 0 and len(inc_id) < 1:
            results = query_db(keyword_esf_sql(keyword, esf_id))

        # if keyword and incident were given
        elif len(keyword) > 0 and len(esf_id) < 1 and len(inc_id) > 0:
            incident = query_db(get_incident_sql(inc_id))[0]
            results = query_db(keyword_incident_sql(keyword, inc_id, distance))

        # if esf and incident were given
        elif len(keyword) < 1 and len(esf_id) > 0 and len(inc_id) > 0:
            incident = query_db(get_incident_sql(inc_id))[0]
            results = query_db(incident_esf_sql(esf_id, inc_id, distance))

        # if all 3 params were given
        elif len(keyword) > 0 and len(esf_id) > 0 and len(inc_id) > 0:
            incident = query_db(get_incident_sql(inc_id))[0]
            results = query_db(all_sql(keyword, esf_id, inc_id, distance))

        # if none of the params were given
        else:
            results = query_db(no_criteria_sql())

        if error is not None:
            return render_template('search_resources.html', esfs=esfs,
                                   incidents=incidents, error=error)
        else:
            return render_template('search_results.html', username=username,
                                   incident=incident, results=results)


def convert_distance(distance):
    """
    Converts distance to a number of use
    :param distance: unicode numberic
    :return: float
    """
    max_distance = 999999

    # ensure distance exists first
    if not distance or not unicode.isnumeric(distance):
        return max_distance

    # convert to float
    distance = float(distance)

    # determine if zero
    delta = .000001
    if distance - delta < delta:
        return max_distance

    # otherwise return float
    return distance


def get_incidents_sql(username):
    """
    Builds sql for querying all incidents
    """
    t = Template("""
        SELECT incident.incident_id, incident.description
        FROM incident
        WHERE incident.username = '$username'
    """)

    return t.substitute({'username': username})


def no_criteria_sql():
    """
    Builds sql query search for no criteria
    """
    t = Template("""
        SELECT DISTINCT resource.resource_id, resource.name, user.name,
            resource.amount, cost_time_period.time_period,
            requests.request_status, requests.return_by_date
        FROM resource
        JOIN user
            ON resource.username = user.username
        JOIN cost_time_period
            ON cost_time_period.cost_time_period_id =
                resource.cost_time_period_id
        LEFT JOIN
            (SELECT resource_id, return_by_date,
                CASE WHEN status = 'Deployed' THEN 'Not Available'
                    ELSE 'Available'
                END AS request_status
            FROM resource_request
            JOIN resource_request_status
                ON resource_request_status.resource_request_status_id =
                    resource_request.resource_request_status_id
            GROUP BY resource_id
            ) requests
            ON requests.resource_id = resource.resource_id
    """)

    return t.substitute()


def keyword_sql(keyword):
    """
    Builds sql query search for keyword only
    """
    t = Template("""
        SELECT DISTINCT resource.resource_id, resource.name, user.name,
            resource.amount, cost_time_period.time_period,
            requests.request_status, requests.return_by_date
        FROM resource
        LEFT JOIN capability
            ON resource.resource_id = capability.resource_id
        JOIN user
            ON resource.username = user.username
        JOIN cost_time_period
        ON cost_time_period.cost_time_period_id =
            resource.cost_time_period_id
        LEFT JOIN
            (SELECT resource_id, return_by_date,
                CASE WHEN status = 'Deployed' THEN 'Not Available'
                    ELSE 'Available'
                END AS request_status
            FROM resource_request
            JOIN resource_request_status
                ON resource_request_status.resource_request_status_id =
                    resource_request.resource_request_status_id
            GROUP BY resource_id
            ) requests
                ON requests.resource_id = resource.resource_id
        WHERE resource.name LIKE '%${keyword}%' OR
            resource.model LIKE '%${keyword}%' OR
            capability.capability LIKE '%${keyword}%'
        ORDER BY requests.request_status, resource.name
    """)
    return t.substitute({'keyword': keyword})


def incident_sql(incident_id, distance):
    """
    Builds sql query search for incidents only
    """
    distance = convert_distance(distance)

    t = Template("""
        SELECT DISTINCT resource.resource_id, resource.name, user.name,
            resource.amount, cost_time_period.time_period,
            requests.request_status, requests.return_by_date,
            distance_formula(resource.latitude, resource.longitude,
                incident_info.latitude, incident_info.longitude) AS distance,
            resource.username
        FROM resource
        JOIN user
            ON resource.username = user.username
        JOIN cost_time_period
            ON cost_time_period.cost_time_period_id =
                resource.cost_time_period_id
        LEFT JOIN
            (SELECT resource_id, return_by_date,
                CASE WHEN status = 'Deployed' THEN 'Not Available'
                    ELSE 'Available'
                END AS request_status
            FROM resource_request
            JOIN resource_request_status
                ON resource_request_status.resource_request_status_id =
                    resource_request.resource_request_status_id
            GROUP BY resource_id
            ) requests
                ON requests.resource_id = resource.resource_id
        CROSS JOIN
            (SELECT incident_id, latitude, longitude
            FROM incident
            WHERE incident_id = $incident_id) incident_info
        WHERE distance_formula(resource.latitude, resource.longitude,
            incident_info.latitude, incident_info.longitude) < $distance
        ORDER BY distance ASC, requests.request_status, resource.name
    """)

    return t.substitute({'incident_id': incident_id, 'distance': distance})


def esf_sql(esf_id):
    """
    Builds sql query search for esf only
    """
    t = Template("""
        SELECT DISTINCT resource.resource_id, resource.name, user.name,
            resource.amount, cost_time_period.time_period,
            requests.request_status, requests.return_by_date
        FROM resource
        LEFT JOIN resource_esf
            ON resource.resource_id = resource_esf.resource_id
        JOIN user
            ON resource.username = user.username
        JOIN cost_time_period
            ON cost_time_period.cost_time_period_id =
                resource.cost_time_period_id
        LEFT JOIN
            (SELECT resource_id, return_by_date,
                CASE WHEN status = 'Deployed' THEN 'Not Available'
                    ELSE 'Available'
                END AS request_status
            FROM resource_request
            JOIN resource_request_status
                ON resource_request_status.resource_request_status_id =
                    resource_request.resource_request_status_id
            GROUP BY resource_id
            ) requests
                ON requests.resource_id = resource.resource_id
        WHERE resource_esf.esf_id = $esf_id OR
            resource.primary_esf_id = $esf_id
        ORDER BY requests.request_status, resource.name
    """)

    return t.substitute({'esf_id': esf_id})


def keyword_esf_sql(keyword, esf_id):
    """
    Builds sql query search for keywords and esfs
    """
    t = Template("""
        SELECT DISTINCT resource.resource_id, resource.name, user.name,
            resource.amount, cost_time_period.time_period,
            requests.request_status, requests.return_by_date
        FROM resource
        LEFT JOIN capability
            ON resource.resource_id = capability.resource_id
        LEFT JOIN resource_esf
            ON resource.resource_id = resource_esf.resource_id
        JOIN user
            ON resource.username = user.username
        JOIN cost_time_period
            ON cost_time_period.cost_time_period_id =
                resource.cost_time_period_id
        LEFT JOIN
            (SELECT resource_id, return_by_date,
                CASE WHEN status = 'Deployed' THEN 'Not Available'
                    ELSE 'Available'
                END AS request_status
            FROM resource_request
            JOIN resource_request_status
                ON resource_request_status.resource_request_status_id =
                    resource_request.resource_request_status_id
            GROUP BY resource_id
            ) requests
                ON requests.resource_id = resource.resource_id
        WHERE (resource.name LIKE '%${keyword}%' OR
            resource.model LIKE '%${keyword}%' OR
            capability.capability LIKE '%${keyword}%') AND
            (resource_esf.esf_id = $esf_id OR resource.primary_esf_id = $esf_id)
        ORDER BY requests.request_status, resource.name
    """)

    return t.substitute({'keyword': keyword, 'esf_id': esf_id})


def incident_esf_sql(esf_id, incident_id, distance):
    """
    Builds sql query search for incidents and esfs
    """
    distance = convert_distance(distance)

    t = Template("""
        SELECT DISTINCT resource.resource_id, resource.name, user.name,
            resource.amount, cost_time_period.time_period,
            requests.request_status, requests.return_by_date,
            distance_formula(resource.latitude, resource.longitude,
                incident_info.latitude, incident_info.longitude) AS distance,
            resource.username
        FROM resource
        LEFT JOIN incident
            ON resource.username = incident.username
        LEFT JOIN resource_esf
            ON resource.resource_id = resource_esf.resource_id
        JOIN user
            ON resource.username = user.username
        JOIN cost_time_period
            ON cost_time_period.cost_time_period_id =
                resource.cost_time_period_id
        LEFT JOIN
            (SELECT resource_id, return_by_date,
                CASE WHEN status = 'Deployed' THEN 'Not Available'
                    ELSE 'Available'
                END AS request_status
            FROM resource_request
            JOIN resource_request_status
                ON resource_request_status.resource_request_status_id =
                    resource_request.resource_request_status_id
            GROUP BY resource_id
            ) requests
        ON requests.resource_id = resource.resource_id
        CROSS JOIN
            (SELECT incident_id, latitude, longitude
            FROM incident
            WHERE incident_id = $incident_id) incident_info
        WHERE distance_formula(resource.latitude, resource.longitude,
            incident_info.latitude, incident_info.longitude) < $distance
            AND (resource_esf.esf_id = $esf_id OR
            resource.primary_esf_id = $esf_id)
        ORDER BY distance ASC, requests.request_status, resource.name
    """)

    return t.substitute({'incident_id': incident_id, 'distance': distance,
                         'esf_id': esf_id})


def keyword_incident_sql(keyword, incident_id, distance):
    """
    Builds sql query search for keywords and incidents
    """
    distance = convert_distance(distance)

    t = Template("""
        SELECT DISTINCT resource.resource_id, resource.name, user.name,
            resource.amount, cost_time_period.time_period,
            requests.request_status, requests.return_by_date,
            distance_formula(resource.latitude, resource.longitude,
                incident_info.latitude, incident_info.longitude) AS distance,
            resource.username
        FROM resource
        LEFT JOIN incident
            ON resource.username = incident.username
        LEFT JOIN capability
            ON resource.resource_id = capability.resource_id
        JOIN user
            ON resource.username = user.username
        JOIN cost_time_period
            ON cost_time_period.cost_time_period_id =
                resource.cost_time_period_id
        LEFT JOIN
            (SELECT resource_id, return_by_date,
                CASE WHEN status = 'Deployed' THEN 'Not Available'
                    ELSE 'Available'
                END AS request_status
            FROM resource_request
            JOIN resource_request_status
                ON resource_request_status.resource_request_status_id =
                    resource_request.resource_request_status_id
            GROUP BY resource_id
            ) requests
                ON requests.resource_id = resource.resource_id
        CROSS JOIN
            (SELECT incident_id, latitude, longitude
            FROM incident
            WHERE incident_id = $incident_id) incident_info
        WHERE distance_formula(resource.latitude, resource.longitude,
            incident_info.latitude, incident_info.longitude) < $distance
            AND (resource.name LIKE '%${keyword}%' OR
            resource.model LIKE '%${keyword}%' OR
            capability.capability LIKE '%${keyword}%')
        ORDER BY distance ASC, requests.request_status, resource.name
    """)

    return t.substitute({'keyword': keyword, 'incident_id': incident_id,
                         'distance': distance})


def all_sql(keyword, esf_id, incident_id, distance):
    """
    Builds sql query search for all criteria
    """
    distance = convert_distance(distance)

    t = Template("""
        SELECT DISTINCT resource.resource_id, resource.name, user.name,
            resource.amount, cost_time_period.time_period,
            requests.request_status, requests.return_by_date,
            distance_formula(resource.latitude, resource.longitude,
                incident_info.latitude, incident_info.longitude) AS distance,
            resource.username
        FROM resource
        LEFT JOIN incident
            ON resource.username = incident.username
        LEFT JOIN capability
            ON resource.resource_id = capability.resource_id
        LEFT JOIN resource_esf
            ON resource.resource_id = resource_esf.resource_id
        JOIN user
            ON resource.username = user.username
        JOIN cost_time_period
            ON cost_time_period.cost_time_period_id =
                resource.cost_time_period_id
        LEFT JOIN
            (SELECT resource_id, return_by_date,
                CASE WHEN status = 'Deployed' THEN 'Not Available'
                    ELSE 'Available'
                END AS request_status
            FROM resource_request
            JOIN resource_request_status
                ON resource_request_status.resource_request_status_id =
                    resource_request.resource_request_status_id
            GROUP BY resource_id
            ) requests
                ON requests.resource_id = resource.resource_id
        CROSS JOIN
            (SELECT incident_id, latitude, longitude
            FROM incident
            WHERE incident_id = $incident_id) incident_info
        WHERE distance_formula(resource.latitude, resource.longitude,
            incident_info.latitude, incident_info.longitude) < $distance
            AND (resource.name LIKE '%${keyword}%' OR
            resource.model LIKE '%${keyword}%' OR
            capability.capability LIKE '%${keyword}%') AND
            (resource_esf.esf_id = $esf_id OR
            resource.primary_esf_id = $esf_id)
        ORDER BY distance ASC, requests.request_status, resource.name
    """)

    return t.substitute({'incident_id': incident_id, 'distance': distance,
                         'esf_id': esf_id, 'keyword': keyword})


def get_incident_sql(incident_id):
    """
    Builds SQL for getting a specific incident
    """
    t = Template("""
        SELECT incident_id, description
        FROM incident
        WHERE incident_id = $incident_id
        LIMIT 1
    """)
    return t.substitute({'incident_id': incident_id})
