"""
Integration tests for search and filtering workflows.
Tests different search combinations and behaviors.
"""

from tests.fixtures.helpers import (
    create_test_cost_period,
    create_test_esf,
    create_test_resource,
    create_test_user,
    insert_cost_period_to_db,
    insert_esf_to_db,
    insert_resource_to_db,
    insert_user_to_db,
)


class TestSearchWorkflows:
    """Test search and filtering behaviors."""

    def test_search_by_esf_only(self, client, clean_db):
        """Test searching resources by ESF only."""
        # Setup test data
        user = create_test_user("searcher", "Resource Searcher", "password")
        esf1 = create_test_esf(1, "Transportation")
        esf2 = create_test_esf(2, "Communications")
        cost_period = create_test_cost_period(1, "Per Hour")
        resource1 = create_test_resource(
            "1234567890", "searcher", "Ambulance", "Ford", "33.7490", "-84.3880", 1, "100.00", 1
        )
        resource2 = create_test_resource(
            "1234567891", "searcher", "Radio", "Motorola", "33.7490", "-84.3880", 1, "50.00", 2
        )

        insert_user_to_db(user)
        insert_esf_to_db(esf1)
        insert_esf_to_db(esf2)
        insert_cost_period_to_db(cost_period)
        insert_resource_to_db(resource1)
        insert_resource_to_db(resource2)

        # Login
        client.post("/login", data={"username": "searcher", "password": "password"})

        # Search by ESF 1 only
        response = client.post("/search-resources", data={"esf": "1"})

        assert response.status_code == 200
        assert "Ambulance" in response.get_data(as_text=True)
        assert "Radio" not in response.get_data(as_text=True)

    def test_search_by_keyword_only(self, client, clean_db):
        """Test searching resources by keyword only."""
        # Setup test data
        user = create_test_user("searcher", "Resource Searcher", "password")
        esf = create_test_esf(1, "Transportation")
        cost_period = create_test_cost_period(1, "Per Hour")
        resource1 = create_test_resource(
            "1234567890",
            "searcher",
            "Emergency Ambulance",
            "Ford",
            "33.7490",
            "-84.3880",
            1,
            "100.00",
            1,
        )
        resource2 = create_test_resource(
            "1234567891", "searcher", "Regular Van", "Chevy", "33.7490", "-84.3880", 1, "75.00", 1
        )

        insert_user_to_db(user)
        insert_esf_to_db(esf)
        insert_cost_period_to_db(cost_period)
        insert_resource_to_db(resource1)
        insert_resource_to_db(resource2)

        # Login
        client.post("/login", data={"username": "searcher", "password": "password"})

        # Search by keyword 'Emergency'
        response = client.post("/search-resources", data={"keyword": "Emergency"})

        assert response.status_code == 200
        assert "Emergency Ambulance" in response.get_data(as_text=True)
        assert "Regular Van" not in response.get_data(as_text=True)

    def test_search_by_distance_only(self, client, clean_db):
        """Test searching resources by distance only."""
        # Setup test data
        user = create_test_user("searcher", "Resource Searcher", "password")
        esf = create_test_esf(1, "Transportation")
        cost_period = create_test_cost_period(1, "Per Hour")
        resource1 = create_test_resource(
            "1234567890",
            "searcher",
            "Nearby Ambulance",
            "Ford",
            "33.7490",
            "-84.3880",
            1,
            "100.00",
            1,
        )
        resource2 = create_test_resource(
            "1234567891", "searcher", "Far Ambulance", "Ford", "35.0000", "-85.0000", 1, "100.00", 1
        )

        insert_user_to_db(user)
        insert_esf_to_db(esf)
        insert_cost_period_to_db(cost_period)
        insert_resource_to_db(resource1)
        insert_resource_to_db(resource2)

        # Login
        client.post("/login", data={"username": "searcher", "password": "password"})

        # Search by distance (should find nearby resources)
        response = client.post("/search-resources", data={"distance": "50"})

        assert response.status_code == 200

    def test_search_combined_filters(self, client, clean_db):
        """Test searching with multiple filters combined."""
        # Setup test data
        user = create_test_user("searcher", "Resource Searcher", "password")
        esf = create_test_esf(1, "Transportation")
        cost_period = create_test_cost_period(1, "Per Hour")
        resource = create_test_resource(
            "1234567890",
            "searcher",
            "Emergency Ford Ambulance",
            "Ford",
            "33.7490",
            "-84.3880",
            1,
            "100.00",
            1,
        )

        insert_user_to_db(user)
        insert_esf_to_db(esf)
        insert_cost_period_to_db(cost_period)
        insert_resource_to_db(resource)

        # Login
        client.post("/login", data={"username": "searcher", "password": "password"})

        # Search with ESF, keyword, and distance
        response = client.post(
            "/search-resources", data={"esf": "1", "keyword": "Ford", "distance": "50"}
        )

        assert response.status_code == 200
        assert "Emergency Ford Ambulance" in response.get_data(as_text=True)

    def test_search_invalid_distance_format(self, client, clean_db):
        """Test search validation with invalid distance format."""
        # Setup test data
        user = create_test_user("searcher", "Resource Searcher", "password")
        esf = create_test_esf(1, "Transportation")

        insert_user_to_db(user)
        insert_esf_to_db(esf)

        # Login
        client.post("/login", data={"username": "searcher", "password": "password"})

        # Search with invalid distance (non-numeric)
        response = client.post("/search-resources", data={"distance": "abc"})

        assert response.status_code == 200
        assert "Distance value must be positive number" in response.get_data(as_text=True)

    def test_search_empty_results(self, client, clean_db):
        """Test search with no matching results."""
        # Setup test data
        user = create_test_user("searcher", "Resource Searcher", "password")
        esf = create_test_esf(1, "Transportation")

        insert_user_to_db(user)
        insert_esf_to_db(esf)

        # Login
        client.post("/login", data={"username": "searcher", "password": "password"})

        # Search for non-existent resource
        response = client.post("/search-resources", data={"keyword": "NonExistentResource"})

        assert response.status_code == 200
        # Should show search form with no results

    def test_search_cancel_workflow(self, client, clean_db):
        """Test canceling search returns to menu."""
        # Setup test data
        user = create_test_user("searcher", "Resource Searcher", "password")

        insert_user_to_db(user)

        # Login
        client.post("/login", data={"username": "searcher", "password": "password"})

        # Cancel search
        response = client.post("/search-resources", data={"cancel": "Cancel"})

        assert response.status_code == 302
        assert "/menu" in response.location
