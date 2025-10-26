"""
Integration tests for search and filtering workflows.
Tests different search combinations and behaviors.
"""

from tests.fixtures.helpers import (
    create_test_resource,
    create_test_user,
    insert_resource_to_db,
    insert_user_to_db,
)


class TestSearchWorkflows:
    """Test search and filtering behaviors."""

    def test_search_by_esf_only(self, client, clean_db):
        # ESF and cost_period are pre-seeded
        user = create_test_user("searcher", "Resource Searcher", "password")
        resource1 = create_test_resource(
            "1234567890", "searcher", "Ambulance", "Ford", "33.7490", "-84.3880", 1, "100.00", 1
        )
        resource2 = create_test_resource(
            "1234567891", "searcher", "Radio", "Motorola", "33.7490", "-84.3880", 1, "50.00", 2
        )

        insert_user_to_db(user)
        insert_resource_to_db(resource1)
        insert_resource_to_db(resource2)

        client.post("/login", data={"username": "searcher", "password": "password"})

        response = client.post("/search-resources/", data={"esf": "1"})

        assert response.status_code == 200
        assert "Ambulance" in response.get_data(as_text=True)
        assert "Radio" not in response.get_data(as_text=True)

    def test_search_by_keyword_only(self, client, clean_db):
        user = create_test_user("searcher", "Resource Searcher", "password")
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
        insert_resource_to_db(resource1)
        insert_resource_to_db(resource2)

        client.post("/login", data={"username": "searcher", "password": "password"})

        response = client.post("/search-resources/", data={"keyword": "Emergency"})

        assert response.status_code == 200
        assert "Emergency Ambulance" in response.get_data(as_text=True)
        assert "Regular Van" not in response.get_data(as_text=True)

    def test_search_by_distance_only(self, client, clean_db):
        user = create_test_user("searcher", "Resource Searcher", "password")
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
        insert_resource_to_db(resource1)
        insert_resource_to_db(resource2)

        client.post("/login", data={"username": "searcher", "password": "password"})

        response = client.post("/search-resources/", data={"distance": "50"})

        assert response.status_code == 200

    def test_search_combined_filters(self, client, clean_db):
        user = create_test_user("searcher", "Resource Searcher", "password")
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
        insert_resource_to_db(resource)

        client.post("/login", data={"username": "searcher", "password": "password"})

        response = client.post(
            "/search-resources/", data={"esf": "1", "keyword": "Ford", "distance": "50"}
        )

        assert response.status_code == 200
        assert "Emergency Ford Ambulance" in response.get_data(as_text=True)

    def test_search_invalid_distance_format(self, client, clean_db):
        # ESF is pre-seeded
        user = create_test_user("searcher", "Resource Searcher", "password")

        insert_user_to_db(user)

        client.post("/login", data={"username": "searcher", "password": "password"})

        response = client.post("/search-resources/", data={"distance": "abc"})

        assert response.status_code == 200
        assert "Distance value must be positive number" in response.get_data(as_text=True)

    def test_search_empty_results(self, client, clean_db):
        # ESF is pre-seeded
        user = create_test_user("searcher", "Resource Searcher", "password")

        insert_user_to_db(user)

        client.post("/login", data={"username": "searcher", "password": "password"})

        response = client.post("/search-resources/", data={"keyword": "NonExistentResource"})

        assert response.status_code == 200
        # Should show search form with no results

    def test_search_cancel_workflow(self, client, clean_db):
        user = create_test_user("searcher", "Resource Searcher", "password")

        insert_user_to_db(user)

        client.post("/login", data={"username": "searcher", "password": "password"})

        response = client.post("/search-resources/", data={"cancel": "Cancel"})

        assert response.status_code == 302
        assert "/menu" in response.location
