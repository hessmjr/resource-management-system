from datetime import datetime, timedelta
from string import Template
from typing import Any

from database import commit_db, get_db, query_db


class SearchResourcesDAL:
    """
    Data Access Layer for Search Resources operations.
    Handles all database interactions for resource search functionality.
    """

    def __init__(self):
        self.db = get_db()

    def get_all_esfs(self) -> list[tuple[Any, ...]]:
        """
        Get all ESFs from database.

        :return: List of ESF tuples from database
        """
        return query_db("SELECT * FROM esf")

    def get_user_incidents(self, username: str) -> list[tuple[Any, ...]]:
        """
        Get all incidents for a specific user.

        :param username: Username to get incidents for
        :return: List of incident tuples
        """
        template = Template("""
            SELECT incident.incident_id, incident.description
            FROM incident
            WHERE incident.username = '$username'
        """)

        sql = template.safe_substitute({'username': username})
        return query_db(sql)

    def search_resources(self, search_params):
        """
        Search resources based on provided parameters.

        :param search_params: Dictionary containing search criteria
        :return: Tuple of (results, incident_info)
        """
        esf_id = search_params['esf_id']
        keyword = search_params['keyword']
        distance = search_params['distance']
        incident_id = search_params['incident_id']

        incident = None

        # Determine which query to use based on parameters
        if len(keyword) > 0 and len(esf_id) < 1 and len(incident_id) < 1:
            results = query_db(self._keyword_sql(keyword))
        elif len(keyword) < 1 and len(esf_id) > 0 and len(incident_id) < 1:
            results = query_db(self._esf_sql(esf_id))
        elif len(keyword) < 1 and len(esf_id) < 1 and len(incident_id) > 0:
            incident = query_db(self._get_incident_sql(incident_id))[0]
            results = query_db(self._incident_sql(incident_id, distance))
        elif len(keyword) > 0 and len(esf_id) > 0 and len(incident_id) < 1:
            results = query_db(self._keyword_esf_sql(keyword, esf_id))
        elif len(keyword) > 0 and len(esf_id) < 1 and len(incident_id) > 0:
            incident = query_db(self._get_incident_sql(incident_id))[0]
            results = query_db(self._keyword_incident_sql(keyword, incident_id, distance))
        elif len(keyword) < 1 and len(esf_id) > 0 and len(incident_id) > 0:
            incident = query_db(self._get_incident_sql(incident_id))[0]
            results = query_db(self._incident_esf_sql(esf_id, incident_id, distance))
        elif len(keyword) > 0 and len(esf_id) > 0 and len(incident_id) > 0:
            incident = query_db(self._get_incident_sql(incident_id))[0]
            results = query_db(self._all_sql(keyword, esf_id, incident_id, distance))
        else:
            results = query_db(self._no_criteria_sql())

        return results, incident

    def create_resource_request(self, resource_id: str, incident_id: str) -> None:
        """
        Create a resource request.

        :param resource_id: ID of the resource to request
        :param incident_id: ID of the incident
        """
        start_date = datetime.now()
        return_date = start_date + timedelta(days=5)

        template = Template("""
            INSERT INTO resource_request (resource_request_status_id, resource_id,
                incident_id, start_date, return_by_date)
            VALUES (1, $resource_id, $incident_id, '$start_date', '$return_date')
        """)

        sql = template.safe_substitute({
            'resource_id': resource_id,
            'incident_id': incident_id,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'return_date': return_date.strftime('%Y-%m-%d')
        })

        commit_db(sql)

    def create_resource_deploy(self, resource_id: str, incident_id: str) -> None:
        """
        Create a resource deploy.

        :param resource_id: ID of the resource to deploy
        :param incident_id: ID of the incident
        """
        start_date = datetime.now()
        return_date = start_date + timedelta(days=5)

        template = Template("""
            INSERT INTO resource_request (resource_request_status_id, resource_id,
                incident_id, start_date, return_by_date)
            VALUES (2, $resource_id, $incident_id, '$start_date', '$return_date')
        """)

        sql = template.safe_substitute({
            'resource_id': resource_id,
            'incident_id': incident_id,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'return_date': return_date.strftime('%Y-%m-%d')
        })

        commit_db(sql)

    def create_resource_repair(self, resource_id: str) -> None:
        """
        Create a resource repair.

        :param resource_id: ID of the resource to repair
        """
        start_date = datetime.now()
        return_date = start_date + timedelta(days=5)

        template = Template("""
            INSERT INTO resource_repair(resource_id, status, start_date,
                ready_by_date)
            VALUES ($resource_id, 'Scheduled', '$start_date', '$ready_date')
        """)

        sql = template.safe_substitute({
            'resource_id': resource_id,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'return_date': return_date.strftime('%Y-%m-%d')
        })

        commit_db(sql)

    def _convert_distance(self, distance: str) -> float:
        """
        Convert distance to a number for use in queries.

        :param distance: Distance string
        :return: Distance as float
        """
        max_distance = 999999

        if not distance or not distance.isdigit():
            return max_distance

        distance = float(distance)

        # determine if zero
        delta = .000001
        if distance - delta < delta:
            return max_distance

        return distance

    def _no_criteria_sql(self) -> str:
        """Build SQL query for no search criteria."""
        template = Template("""
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
                    CASE WHEN status = 'Deployed' or CURRENT_DATE < return_by_date
                        THEN 'Not Available'
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

        return template.substitute()

    def _keyword_sql(self, keyword: str) -> str:
        """Build SQL query for keyword search only."""
        template = Template("""
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
                    CASE WHEN status = 'Deployed' or CURRENT_DATE < return_by_date
                        THEN 'Not Available'
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

        return template.substitute({'keyword': keyword})

    def _esf_sql(self, esf_id: str) -> str:
        """Build SQL query for ESF search only."""
        template = Template("""
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
                    CASE WHEN status = 'Deployed' or CURRENT_DATE < return_by_date
                        THEN 'Not Available'
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

        return template.substitute({'esf_id': esf_id})

    def _incident_sql(self, incident_id: str, distance: str) -> str:
        """Build SQL query for incident search only."""
        distance = self._convert_distance(distance)

        template = Template("""
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
                    CASE WHEN status = 'Deployed' or CURRENT_DATE < return_by_date
                        THEN 'Not Available'
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

        return template.substitute({'incident_id': incident_id, 'distance': distance})

    def _keyword_esf_sql(self, keyword: str, esf_id: str) -> str:
        """Build SQL query for keyword and ESF search."""
        template = Template("""
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
                    CASE WHEN status = 'Deployed' or CURRENT_DATE < return_by_date
                        THEN 'Not Available'
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

        return template.substitute({'keyword': keyword, 'esf_id': esf_id})

    def _keyword_incident_sql(self, keyword: str, incident_id: str, distance: str) -> str:
        """Build SQL query for keyword and incident search."""
        distance = self._convert_distance(distance)

        template = Template("""
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
                    CASE WHEN status = 'Deployed' or CURRENT_DATE < return_by_date
                        THEN 'Not Available'
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

        return template.substitute({
            'keyword': keyword,
            'incident_id': incident_id,
            'distance': distance
        })

    def _incident_esf_sql(self, esf_id: str, incident_id: str, distance: str) -> str:
        """Build SQL query for incident and ESF search."""
        distance = self._convert_distance(distance)

        template = Template("""
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
                    CASE WHEN status = 'Deployed' or CURRENT_DATE < return_by_date
                        THEN 'Not Available'
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

        return template.substitute({
            'incident_id': incident_id,
            'distance': distance,
            'esf_id': esf_id
        })

    def _all_sql(self, keyword: str, esf_id: str, incident_id: str, distance: str) -> str:
        """Build SQL query for all search criteria."""
        distance = self._convert_distance(distance)

        template = Template("""
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
                    CASE WHEN status = 'Deployed' or CURRENT_DATE < return_by_date
                        THEN 'Not Available'
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

        return template.substitute({
            'incident_id': incident_id,
            'distance': distance,
            'esf_id': esf_id,
            'keyword': keyword
        })

    def _get_incident_sql(self, incident_id: str) -> str:
        """Build SQL for getting a specific incident."""
        template = Template("""
            SELECT incident_id, description
            FROM incident
            WHERE incident_id = $incident_id
            LIMIT 1
        """)

        return template.substitute({'incident_id': incident_id})
