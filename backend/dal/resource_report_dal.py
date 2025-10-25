from string import Template
from typing import Any

from database import get_db, query_db


class ResourceReportDAL:
    """
    Data Access Layer for Resource Report operations.
    Handles all database interactions for resource reporting.
    """

    def __init__(self):
        self.db = get_db()

    def get_resource_report(self, username: str) -> list[tuple[Any, ...]]:
        """
        Get resource report data for a specific user.

        :param username: Username to get report for
        :return: List of report tuples
        """
        template = Template("""
            SELECT esf.esf_id, esf.description, IF(totals.total, totals.total, 0)
                AS `Total Resources`, IF(used.in_use, used.in_use, 0) AS `In Use`
            FROM esf
            LEFT JOIN resource
                ON esf.esf_id = resource.primary_esf_id
            LEFT JOIN
                    (SELECT COUNT(resource.resource_id) AS total,
                        resource.primary_esf_id AS p_esf_id
                    FROM resource
                    WHERE resource.username = '$username'
                    GROUP BY resource.primary_esf_id) totals
                ON esf.esf_id = totals.p_esf_id
            LEFT JOIN
                    (SELECT COUNT(resource.primary_esf_id) AS in_use,
                        resource.primary_esf_id AS req_esf_id
                    FROM resource
                    JOIN resource_request
                        ON resource.resource_id = resource_request.resource_id
                    WHERE resource_request.resource_request_status_id = 2
                        AND resource.username = '$username'
                    GROUP BY resource.primary_esf_id) used
                ON esf.esf_id = used.req_esf_id
            GROUP BY esf.esf_id
        """)

        sql = template.substitute({'username': username})
        return query_db(sql)
