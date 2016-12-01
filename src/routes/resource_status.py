from string import Template

from flask import render_template, request, session

from src.database import query_db, commit_db


def resource_status_route(error=None):
    """
    Builds the template for user resource status
    :return: rendered template
    """
    username = session.get('username')

    # if user deployed a resource
    if '/deploy' in request.url:
        update_resource_status(deploy_sql())

    # if user returned a resource
    elif '/return' in request.url:
        update_resource_status(return_sql())

    # if user rejected a resource
    elif '/reject' in request.url:
        update_resource_status(reject_sql())

    # if user canceled a request for a resource
    elif '/request/cancel' in request.url:
        update_resource_status(cancel_request_sql())

    # if user canceled a resource repair
    elif '/repair/cancel' in request.url:
        update_resource_status(cancel_repair_sql())

    # query to get the statuses of user resources
    in_use = query_db(in_use_sql(username))
    requested = query_db(requested_sql(username))
    requests_recvd = query_db(requests_recieved_sql(username))
    repairs = query_db(in_repair_sql(username))

    # return rendered template to user with any errors
    return render_template('resource_status.html', resources_in_use=in_use,
                           resources_requested=requested,
                           resource_requests_received=requests_recvd,
                           resource_repairs=repairs, error=error)


def update_resource_status(sql_template):
    """
    Updates the database with the given SQL statement
    :param sql_template - SQL template to use for updateing
    :return: redirect to resource status page
    """
    # get requested resource ID
    req_id = request.args.get('id', '')

    # if ID isn't blank create query and update database
    if req_id != '':
        query = sql_template.safe_substitute({'resource_request_id': req_id})
        commit_db(query)


def in_use_sql(username):
    """
    Builds SQL for getting resources currently in use
    """
    t = Template("""
        SELECT resource.resource_id, resource.name, incident.description,
            user.name as resource_owner, resource_request.start_date,
            resource_request.return_by_date,
            resource_request.resource_request_id
        FROM resource_request
        JOIN incident
            ON resource_request.incident_id = incident.incident_id
        JOIN resource
            ON resource_request.resource_id = resource.resource_id
        JOIN user
            ON resource.username = user.username
        JOIN resource_request_status rr_status
            ON rr_status.resource_request_status_id =
                resource_request.resource_request_status_id
        WHERE incident.username = '$username' AND rr_status.status = 'Deployed'
    """)

    return t.safe_substitute({'username': username})


def requested_sql(username):
    """
    Builds SQL for getting resources that have been requested by the user
    """
    t = Template("""
        SELECT resource.resource_id, resource.name, incident.description,
            user.name as resource_owner, resource_request.return_by_date,
            resource_request.resource_request_id
        FROM resource_request
        JOIN incident
            ON resource_request.incident_id = incident.incident_id
        JOIN resource
            ON resource_request.resource_id = resource.resource_id
        JOIN user
            ON resource.username = user.username
        JOIN resource_request_status rr_status
            ON rr_status.resource_request_status_id =
                resource_request.resource_request_status_id
        WHERE incident.username = '$username' AND rr_status.status = 'New'
    """)

    return t.safe_substitute({'username': username})


def requests_recieved_sql(username):
    """
    Builds SQL for getting resources that have been requested from the user
    """
    t = Template("""
        SELECT resource.resource_id, resource.name, incident.description,
            incident_owner.name, resource_request.return_by_date,
            resource_request.resource_request_id, rr_status.status
        FROM resource_request
        JOIN incident
            ON resource_request.incident_id = incident.incident_id
        JOIN resource
            ON resource_request.resource_id = resource.resource_id
        JOIN user as incident_owner
            ON incident.username = incident_owner.username
        JOIN resource_request_status rr_status
            ON rr_status.resource_request_status_id =
                resource_request.resource_request_status_id
        WHERE resource.username = '$username' AND rr_status.status IN ('New')
    """)

    return t.safe_substitute({'username': username})


def in_repair_sql(username):
    """
    Builds SQL for getting resources that are currently under repair
    """
    t = Template("""
        SELECT resource.resource_id, resource.name, resource_repair.start_date,
            resource_repair.ready_by_date, resource_repair.resource_repair_id,
            resource_repair.status
        FROM resource_repair
        JOIN resource
            ON resource_repair.resource_id = resource.resource_id
        WHERE resource.username = '$username'
            AND resource_repair.status != 'Cancelled'
    """)

    return t.safe_substitute({'username': username})


def deploy_sql():
    """
    Builds a SQL template for deploying a resource
    """
    t = Template("""
        UPDATE resource_request
        SET resource_request.resource_request_status_id =
            (SELECT resource_request_status_id
            FROM resource_request_status
            WHERE status = 'Deployed')
        WHERE resource_request_id = $resource_request_id
    """)

    return t


def return_sql():
    """
    Builds SQL template for returning resources that are in use
    """
    t = Template("""
        UPDATE resource_request
        SET resource_request.resource_request_status_id =
            (SELECT resource_request_status_id
            FROM resource_request_status
            WHERE status = 'Returned')
        WHERE resource_request_id = $resource_request_id
    """)

    return t


def reject_sql():
    """
    Builds a SQL template for rejecting a resource
    """
    t = Template("""
        UPDATE resource_request
        SET resource_request.resource_request_status_id =
            (SELECT resource_request_status_id
            FROM resource_request_status
            WHERE status = 'Rejected')
        WHERE resource_request_id = $resource_request_id
    """)

    return t


def cancel_request_sql():
    """
    Builds SQL template for cancel a resource request
    """
    t = Template("""
        UPDATE resource_request
        SET resource_request.resource_request_status_id =
            (SELECT resource_request_status_id
            FROM resource_request_status
            WHERE status = 'Rejected')
        WHERE resource_request_id = $resource_request_id
    """)

    return t


def cancel_repair_sql():
    """
    Builds a SQL template for canceling a repair
    """
    t = Template("""
        UPDATE resource_repair
        SET resource_repair.status = 'Cancelled'
        WHERE resource_repair_id = $resource_repair_id
    """)

    return t
