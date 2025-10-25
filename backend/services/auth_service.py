"""
Authentication service for handling login/logout logic.
"""

import bcrypt
from flask import redirect, session, url_for
from dal.user_dal import UserDAL


class AuthService:
    """Handles authentication business logic."""

    def __init__(self):
        """Initialize with user DAL."""
        self.user_dal = UserDAL()

    def authenticate_user(self, username: str, password: str) -> str | None:
        """
        Authenticate user credentials.

        :param username: Username to authenticate
        :param password: Password to verify
        :return: Error message if authentication fails, None if successful
        """
        if not username or not password:
            return 'Username and password are required'

        user = self.user_dal.get_user_by_username(username)

        if user is None:
            return 'Invalid username'

        if not self._verify_password(password, user[2]):
            return 'Invalid password'

        # Set session data
        session['username'] = user[0]
        session['name'] = user[1]

        return None

    def logout_user(self) -> None:
        """Clear user session."""
        session.clear()

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify password against hash.

        Supports both bcrypt hashes and legacy plaintext passwords.

        :param password: Plain text password
        :param hashed_password: Stored password hash
        :return: True if password matches, False otherwise
        """
        if hashed_password.startswith('$2b$'):
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        else:
            return password == hashed_password
