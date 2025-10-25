"""
Integration tests for authentication workflows.
Tests complete user authentication behaviors.
"""

from tests.fixtures.helpers import create_test_user, insert_user_to_db


class TestAuthenticationFlow:
    """Test complete authentication workflows."""

    def test_failed_login_invalid_username(self, client, clean_db):
        """Test login with non-existent username."""
        # Setup test data
        user = create_test_user("validuser", "Valid User", "password")
        insert_user_to_db(user)

        # Attempt login with invalid username
        response = client.post("/login", data={"username": "invaliduser", "password": "password"})

        assert response.status_code == 200
        assert "Invalid username" in response.get_data(as_text=True)

    def test_failed_login_invalid_password(self, client, clean_db):
        """Test login with wrong password."""
        # Setup test data
        user = create_test_user("testuser", "Test User", "password")
        insert_user_to_db(user)

        # Attempt login with wrong password
        response = client.post("/login", data={"username": "testuser", "password": "wrongpassword"})

        assert response.status_code == 200
        assert "Invalid password" in response.get_data(as_text=True)

    def test_successful_login_and_session(self, client, clean_db):
        """Test successful login and session management."""
        # Setup test data
        user = create_test_user("testuser", "Test User", "password")
        insert_user_to_db(user)

        # Successful login
        response = client.post("/login", data={"username": "testuser", "password": "password"})

        assert response.status_code == 302
        assert "/menu" in response.location

        # Verify session was set
        with client.session_transaction() as sess:
            assert sess["username"] == "testuser"
            assert sess["name"] == "Test User"

    def test_protected_page_access_after_login(self, client, clean_db):
        """Test accessing protected pages after login."""
        # Setup test data
        user = create_test_user("testuser", "Test User", "password")
        insert_user_to_db(user)

        # Login
        client.post("/login", data={"username": "testuser", "password": "password"})

        # Access protected page
        response = client.get("/menu")
        assert response.status_code == 200

    def test_protected_page_access_without_login(self, client, clean_db):
        """Test accessing protected pages without login redirects to login."""
        # Try to access protected page without login
        response = client.get("/menu", follow_redirects=True)

        assert "/login" in response.location or "/login" in response.get_data(as_text=True)

    def test_logout_clears_session(self, client, clean_db):
        """Test logout clears session and redirects."""
        # Setup test data
        user = create_test_user("testuser", "Test User", "password")
        insert_user_to_db(user)

        # Login
        client.post("/login", data={"username": "testuser", "password": "password"})

        # Verify session exists
        with client.session_transaction() as sess:
            assert "username" in sess

        # Logout
        response = client.get("/logout")
        assert response.status_code == 302

        # Verify session is cleared
        with client.session_transaction() as sess:
            assert "username" not in sess

    def test_access_protected_page_after_logout(self, client, clean_db):
        """Test accessing protected page after logout redirects to login."""
        # Setup test data
        user = create_test_user("testuser", "Test User", "password")
        insert_user_to_db(user)

        # Login
        client.post("/login", data={"username": "testuser", "password": "password"})

        # Logout
        client.get("/logout")

        # Try to access protected page
        response = client.get("/menu", follow_redirects=True)
        assert "/login" in response.location or "/login" in response.get_data(as_text=True)

    def test_empty_credentials_validation(self, client, clean_db):
        """Test validation of empty username/password."""
        # Test empty username
        response = client.post("/login", data={"username": "", "password": "password"})
        assert response.status_code == 200
        assert "Username and password are required" in response.get_data(as_text=True)

        # Test empty password
        response = client.post("/login", data={"username": "testuser", "password": ""})
        assert response.status_code == 200
        assert "Username and password are required" in response.get_data(as_text=True)

        # Test both empty
        response = client.post("/login", data={"username": "", "password": ""})
        assert response.status_code == 200
        assert "Username and password are required" in response.get_data(as_text=True)
