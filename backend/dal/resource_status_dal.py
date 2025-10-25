from string import Template
from typing import Any

from database import commit_db, get_db, query_db


class ResourceStatusDAL:
    """
    Data Access Layer for Resource Status operations.
    Handles all database interactions for resource status management.
    """

    def __init__(self):
        self.db = get_db()

    def get_resources_in_use(self, username: str) -> list[tuple[Any, ...]]:
        """
        Get resources currently in use by the user.

        :param username: Username to get resources for
        :return: List of resource tuples
        """
        template = Template("""
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

        sql = template.safe_substitute({"username": username})
        return query_db(sql)

    def get_resources_requested(self, username: str) -> list[tuple[Any, ...]]:
        """
        Get resources that have been requested by the user.

        :param username: Username to get resources for
        :return: List of resource tuples
        """
        template = Template("""
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

        sql = template.safe_substitute({"username": username})
        return query_db(sql)

    def get_resource_requests_received(self, username: str) -> list[tuple[Any, ...]]:
        """
        Get resources that have been requested from the user.

        :param username: Username to get requests for
        :return: List of resource request tuples
        """
        template = Template("""
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

        sql = template.safe_substitute({"username": username})
        return query_db(sql)

    def get_resources_in_repair(self, username: str) -> list[tuple[Any, ...]]:
        """
        Get resources that are currently under repair.

        :param username: Username to get repairs for
        :return: List of repair tuples
        """
        template = Template("""
            SELECT resource.resource_id, resource.name, resource_repair.start_date,
                resource_repair.ready_by_date, resource_repair.resource_repair_id,
                resource_repair.status
            FROM resource_repair
            JOIN resource
                ON resource_repair.resource_id = resource.resource_id
            WHERE resource.username = '$username'
                AND resource_repair.status != 'Cancelled'
        """)

        sql = template.safe_substitute({"username": username})
        return query_db(sql)

    def update_resource_status(self, action: str, resource_request_id: str) -> None:
        """
        Update resource status based on action.

        :param action: Action to perform (deploy, return, reject, etc.)
        :param resource_request_id: ID of the resource request to update
        """
        if action == "deploy":
            self._deploy_resource(resource_request_id)
        elif action == "return":
            self._return_resource(resource_request_id)
        elif action == "reject":
            self._reject_resource(resource_request_id)
        elif action == "cancel_request":
            self._cancel_request(resource_request_id)
        elif action == "cancel_repair":
            self._cancel_repair(resource_request_id)

    def _deploy_resource(self, resource_request_id: str) -> None:
        """Deploy a resource."""
        template = Template("""
            UPDATE resource_request
            SET resource_request.resource_request_status_id =
                (SELECT resource_request_status_id
                FROM resource_request_status
                WHERE status = 'Deployed')
            WHERE resource_request_id = $resource_request_id
        """)

        sql = template.safe_substitute({"resource_request_id": resource_request_id})
        commit_db(sql)

    def _return_resource(self, resource_request_id: str) -> None:
        """Return a resource."""
        template = Template("""
            UPDATE resource_request
            SET resource_request.resource_request_status_id =
                (SELECT resource_request_status_id
                FROM resource_request_status
                WHERE status = 'Returned')
            WHERE resource_request_id = $resource_request_id
        """)

        sql = template.safe_substitute({"resource_request_id": resource_request_id})
        commit_db(sql)

    def _reject_resource(self, resource_request_id: str) -> None:
        """Reject a resource."""
        template = Template("""
            UPDATE resource_request
            SET resource_request.resource_request_status_id =
                (SELECT resource_request_status_id
                FROM resource_request_status
                WHERE status = 'Rejected')
            WHERE resource_request_id = $resource_request_id
        """)

        sql = template.safe_substitute({"resource_request_id": resource_request_id})
        commit_db(sql)

    def _cancel_request(self, resource_request_id: str) -> None:
        """Cancel a resource request."""
        template = Template("""
            UPDATE resource_request
            SET resource_request.resource_request_status_id =
                (SELECT resource_request_status_id
                FROM resource_request_status
                WHERE status = 'Rejected')
            WHERE resource_request_id = $resource_request_id
        """)

        sql = template.safe_substitute({"resource_request_id": resource_request_id})
        commit_db(sql)

    def _cancel_repair(self, resource_repair_id: str) -> None:
        """Cancel a resource repair."""
        template = Template("""
            UPDATE resource_repair
            SET resource_repair.status = 'Cancelled'
            WHERE resource_repair_id = $resource_repair_id
        """)

        sql = template.safe_substitute({"resource_repair_id": resource_repair_id})
        commit_db(sql)
