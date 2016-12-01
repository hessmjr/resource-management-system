from string import Template

from flask import render_template, session

from src.database import query_db


def resource_report_route():
    """
    Renders the owner's resource report
    :return: rendered template
    """
    # get current user
    username = session.get('username')

    # query database for report information
    results = query_db(resource_report_query(username))

    return render_template('resource_report.html', results=results)


def resource_report_query(username):
    t = Template("""
        SELECT `esf`.`esf_id`, `esf`.`description`, IF(`totals`.`total`,
            `totals`.`total`, 0), IF(`used`.`in_use`, `used`.`in_use`, 0)
        FROM `esf`
        LEFT JOIN `resource`
        ON `esf`.`esf_id` = `resource`.`primary_esf_id`
        LEFT JOIN
            (SELECT COUNT(`resource`.`resource_id`) AS total,
            `resource`.`primary_esf_id` AS p_esf_id
            FROM `resource`
            WHERE `resource`.`username` = '$username'
            GROUP BY `resource`.`primary_esf_id`) totals
        ON `esf`.`esf_id` = `totals`.`p_esf_id`
        LEFT JOIN
            (SELECT COUNT(`resource`.`primary_esf_id`) AS `in_use`,
                `resource`.`primary_esf_id` AS `req_esf_id`
            FROM `resource`
            JOIN `resource_request`
            ON `resource`.`resource_id` = `resource_request`.`resource_id`
            WHERE `resource_request`.`resource_request_status_id` = 2
                AND `resource`.`username` = '$username'
            GROUP BY `resource`.`primary_esf_id`) used
        ON `esf`.`esf_id` = `used`.`req_esf_id`
        GROUP BY `esf`.`esf_id`
    """)
    return t.substitute({'username': username})
