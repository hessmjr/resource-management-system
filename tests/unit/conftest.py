"""
Unit test configuration - no Flask dependencies.
"""
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add backend directory to Python path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))


@pytest.fixture
def mock_auth_service():
    """Create AuthService with mocked dependencies."""
    from services.auth_service import AuthService

    # Mock the UserDAL import to avoid database connection
    with patch('services.auth_service.UserDAL') as mock_dal_class:
        mock_dal_instance = Mock()
        mock_dal_class.return_value = mock_dal_instance

        service = AuthService()
        return service
