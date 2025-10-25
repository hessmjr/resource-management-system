from string import Template

from database import commit_db, get_db


class AddIncidentDAL:
    """
    Data Access Layer for Add Incident operations.
    Handles all database interactions for incident creation.
    """

    def __init__(self):
        self.db = get_db()

    def create_incident(self, form_data, username):
        """
        Create a new incident in the database.

        :param form_data: Form data containing incident details
        :param username: Username of the incident owner
        """
        template = Template("""
            INSERT INTO incident
            VALUES ('$incident_id', '$username', '$description','$latitude',
                '$longitude', '$incident_date')
        """)

        sql = template.safe_substitute({
            'incident_id': form_data['incident_id'],
            'username': username,
            'description': form_data['description'],
            'latitude': form_data['lat'],
            'longitude': form_data['lng'],
            'incident_date': form_data['date']
        })

        commit_db(sql)
