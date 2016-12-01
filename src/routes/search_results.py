from datetime import datetime, timedelta
from string import Template

from flask import redirect, url_for

from src.database import commit_db


def user_request(inc_id, res_id):
    """

    :param inc_id:
    :param res_id:
    :return:
    """

    start_date = datetime.now()
    return_date = start_date + timedelta(days=5)

    t = Template("""
        INSERT INTO resource_request (resource_request_status_id, resource_id,
        incident_id, start_date, return_by_date)
        VALUES (1, $resource_id, $incident_id, '$start_date', '$return_date')
    """)
    query = t.safe_substitute({'resource_id': res_id, 'incident_id': inc_id,
                              'start_date': start_date.strftime('%Y-%m-%d'),
                              'return_date': return_date.strftime('%Y-%m-%d')})

    commit_db(query)
    return redirect(url_for('resource_status'))

def owner_deploy(inc_id, res_id):
    # values for inserting into resource_request table in db

    start_date = datetime.now()
    return_date = start_date + timedelta(days=5)

    t = Template("""
      INSERT INTO resource_request (resource_request_status_id, resource_id, incident_id, start_date, return_by_date)
      VALUES (2, $resource_id, $incident_id, '$start_date', '$return_date')
    """)
    commit_db(t.safe_substitute({'resource_id': res_id, 'incident_id': inc_id, 'start_date': start_date.strftime('%Y-%m-%d'), 'return_date': return_date.strftime('%Y-%m-%d')}))
    return redirect(url_for('resource_status'))


def owner_repair(res_id):
    # values for inserting into resource_request table in db

    start_date = datetime.now()
    return_date = start_date + timedelta(days=5)

    t = Template("""
        INSERT INTO resource_repair(resource_id, status, start_date, ready_by_date)
        VALUES ($resource_id, 'Scheduled', '$start_date', '$ready_date')
    """)
    commit_db(t.safe_substitute({'resource_id': res_id, 'start_date': start_date.strftime('%Y-%m-%d'), 'return_date': return_date.strftime('%Y-%m-%d')}))
    return redirect(url_for('resource_status'))
