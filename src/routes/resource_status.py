from string import Template

from flask import render_template, request, redirect, url_for, session

from src.database import query_db, commit_db


def get_resource_status_route():
    username = session.get('username')
    # Resources in Use
    resources_in_use = query_db(get_resources_in_use_query(username))

    # Resources Requested by User
    resources_requested = query_db(get_resources_requested_by_user_query(username))

    # Resource Requests received by User
    resource_requests_received = query_db(get_resource_requests_received_by_user_query(username))

    # Repairs Scheduled/In-progress
    resource_repairs = query_db(get_resources_in_repair_query(username))

    return render_template('resource_status.html', resources_in_use=resources_in_use,
                           resources_requested=resources_requested,
                           resource_requests_received=resource_requests_received,
                           resource_repairs=resource_repairs)


def return_resource_in_use():
    resource_request_id = request.args.get('id', '')
    if resource_request_id != '':
        commit_db(get_return_resource_query(resource_request_id=resource_request_id))

    return redirect(url_for('resource_status'))


def cancel_resource_request_for_resource():
    resource_request_id = request.args.get('id', '')
    if resource_request_id != '':
        commit_db(get_cancel_resource_request_query(resource_request_id=resource_request_id))

    return redirect(url_for('resource_status'))


def deploy_resource_from_request():
    resource_request_id = request.args.get('id', '')
    if resource_request_id != '':
        commit_db(get_deploy_resource_query(resource_request_id=resource_request_id))
    return redirect(url_for('resource_status'))


def reject_resource_from_request():
    resource_request_id = request.args.get('id', '')
    if resource_request_id != '':
        commit_db(get_reject_resource_query(resource_request_id=resource_request_id))
    return redirect(url_for('resource_status'))


def cancel_request_for_resource_repair():
    resource_repair_id = request.args.get('id', '')
    if resource_repair_id != '':
        commit_db(get_cancel_resource_repair_query(resource_repair_id=resource_repair_id))
    return redirect(url_for('resource_status'))


def get_resources_in_use_query(username):
    t = Template("""
                SELECT
              resource.resource_id,
              resource.name,
              incident.description,
              user.name as resource_owner,
              resource_request.start_date,
              resource_request.return_by_date,
              resource_request.resource_request_id
            FROM
              resource_request
              JOIN
              incident ON resource_request.incident_id = incident.incident_id
              JOIN
              resource ON resource_request.resource_id = resource.resource_id
              JOIN user
              ON resource.username = user.username
              JOIN resource_request_status rr_status
                ON rr_status.resource_request_status_id = resource_request.resource_request_status_id
            WHERE incident.username = '$username' AND rr_status.status = 'Deployed'
    """)
    return t.safe_substitute({'username': username})


def get_resources_requested_by_user_query(username):
    t = Template("""
        SELECT
  resource.resource_id,
  resource.name,
  incident.description,
  user.name as resource_owner,
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
    ON rr_status.resource_request_status_id = resource_request.resource_request_status_id
WHERE incident.username = '$username'
    AND rr_status.status = 'New'
    """)
    return t.safe_substitute({'username': username})


def get_resource_requests_received_by_user_query(username):
    t = Template("""
    SELECT
  resource.resource_id,
  resource.name,
  incident.description,
  incident_owner.name,
  resource_request.return_by_date,
  resource_request.resource_request_id,
  rr_status.status
FROM resource_request
  JOIN incident
    ON resource_request.incident_id = incident.incident_id
  JOIN resource
    ON resource_request.resource_id = resource.resource_id
  JOIN user as incident_owner
    ON incident.username = incident_owner.username
  JOIN resource_request_status rr_status
    ON rr_status.resource_request_status_id = resource_request.resource_request_status_id
WHERE resource.username = '$username'
    AND rr_status.status IN ('New')
    """)
    return t.safe_substitute({'username': username})


def get_resources_in_repair_query(username):
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


def get_return_resource_query(resource_request_id):
    t = Template("""
            UPDATE resource_request
            SET resource_request.resource_request_status_id =
                (SELECT resource_request_status_id
                 FROM resource_request_status
                 WHERE status = 'Returned')
            WHERE resource_request_id = $resource_request_id
    """)

    return t.safe_substitute({'resource_request_id': resource_request_id})


def get_cancel_resource_request_query(resource_request_id):
    t = Template("""
        UPDATE resource_request
        SET resource_request.resource_request_status_id =
            (SELECT resource_request_status_id
              FROM resource_request_status
              WHERE status = 'Rejected')
        WHERE resource_request_id = $resource_request_id

    """)
    return t.safe_substitute({'resource_request_id': resource_request_id})


def get_deploy_resource_query(resource_request_id):
    t = Template("""
        UPDATE resource_request
        SET resource_request.resource_request_status_id =
          (SELECT resource_request_status_id
            FROM resource_request_status
            WHERE status = 'Deployed')
        WHERE resource_request_id = $resource_request_id
    """)
    return t.safe_substitute({'resource_request_id': resource_request_id})


def get_reject_resource_query(resource_request_id):
    t = Template("""
        UPDATE resource_request
        SET resource_request.resource_request_status_id =
          (SELECT resource_request_status_id
            FROM resource_request_status
            WHERE status = 'Rejected')
        WHERE resource_request_id = $resource_request_id
    """)
    return t.safe_substitute({'resource_request_id': resource_request_id})


def get_cancel_resource_repair_query(resource_repair_id):
    t = Template("""
        UPDATE resource_repair
        SET resource_repair.status = 'Cancelled'
        WHERE resource_repair_id = $resource_repair_id
    """)
    return t.safe_substitute({'resource_repair_id': resource_repair_id})
