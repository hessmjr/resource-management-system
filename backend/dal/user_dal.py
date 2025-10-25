"""
Data Access Layer for user-related database operations.
"""

from database import get_db


class UserDAL:
    """Handles user database operations."""

    def __init__(self):
        """Initialize with database connection."""
        self.db = get_db()

    def get_user_by_username(self, username: str) -> tuple | None:
        """
        Retrieve user by username.

        :param username: The username to search for
        :return: User tuple (id, name, password) or None if not found
        """
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.fetchall()  # Consume any remaining results
        cursor.close()
        return result
