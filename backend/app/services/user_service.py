"""User service for managing user-related database operations."""

import hashlib
from ..config import query_db, execute_db


class UserService:
    """Service class for user-related operations."""
    
    @staticmethod
    def authenticate_user(username, password):
        """Authenticate a user with username and password."""
        query = "SELECT * FROM user WHERE username = %s"
        user = query_db(query, (username,))
        
        if not user or len(user) < 1:
            return None
            
        # Hash the provided password for comparison
        password_hash = UserService._hash_password(password)
        
        # Check password hash
        if user[0][2] != password_hash:
            return None
            
        return {
            'username': user[0][0],
            'name': user[0][1],
            'password': user[0][2]
        }
    
    @staticmethod
    def _hash_password(password):
        """Hash a password using SHA-256 (in production, use bcrypt or similar)."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def get_user_details(username):
        """Get detailed user information including user type specific data."""
        query = """
            SELECT
                user.name, company.headquarters, government_agency.jurisdiction,
                municipality.population_size, individual.job_title,
                individual.hired_date
            FROM user
            LEFT JOIN company
                ON company.username = user.username
            LEFT JOIN government_agency
                ON government_agency.username = user.username
            LEFT JOIN municipality
                ON municipality.username = user.username
            LEFT JOIN individual
                ON individual.username = user.username
            WHERE user.username = %s
        """
        
        result = query_db(query, (username,))
        if not result or len(result) < 1:
            return {}
            
        user_details = result[0]
        details = {}
        
        # Map results to dictionary, excluding None values
        field_names = ['name', 'headquarters', 'jurisdiction', 'population_size', 'job_title', 'hired_date']
        for i, value in enumerate(user_details):
            if value is not None:
                details[field_names[i]] = value
                
        return details