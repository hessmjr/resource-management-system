"""Incident service for managing incident-related database operations."""

from ..config import query_db, execute_db


class IncidentService:
    """Service class for incident-related operations."""
    
    @staticmethod
    def get_user_incidents(username):
        """Get all incidents for a specific user."""
        query = """
            SELECT incident.incident_id, incident.description
            FROM incident
            WHERE incident.username = %s
        """
        return query_db(query, (username,))
    
    @staticmethod
    def get_incident_by_id(incident_id):
        """Get a specific incident by ID."""
        query = """
            SELECT incident_id, description, latitude, longitude
            FROM incident
            WHERE incident_id = %s
            LIMIT 1
        """
        result = query_db(query, (incident_id,))
        return result[0] if result else None
    
    @staticmethod
    def create_incident(incident_data):
        """Create a new incident."""
        incident_id = incident_data['incident_id']
        username = incident_data['username']
        description = incident_data['description']
        latitude = incident_data['latitude']
        longitude = incident_data['longitude']
        incident_date = incident_data['incident_date']
        
        query = """
            INSERT INTO incident
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute_db(query, (incident_id, username, description, latitude, longitude, incident_date))
        return incident_id