"""
Integration tests for resource management workflows.
Tests complete resource lifecycle behaviors.
"""

from tests.fixtures.helpers import (
    create_test_incident,
    create_test_resource,
    create_test_user,
    insert_incident_to_db,
    insert_resource_to_db,
    insert_user_to_db,
)


class TestResourceLifecycle:
    """Test complete resource management workflows."""

    def test_add_resource_workflow(self, client, clean_db):
        """Test adding a new resource."""
        # Setup test data
        user = create_test_user("resourceowner", "Resource Owner", "password")
        insert_user_to_db(user)

        # Login
        client.post("/login", data={"username": "resourceowner", "password": "password"})

        # Add resource
        response = client.post(
            "/add-resource/",
            data={
                "resource_name": "Test Ambulance",
                "model": "Ford",
                "latitude": "33.7490",
                "longitude": "-84.3880",
                "cost": "100.00",
                "esf_id": "1",
                "cost_time_period_id": "1",
            },
        )

        assert response.status_code == 302
        assert "/menu" in response.location

    def test_search_resources_by_esf(self, client, clean_db):
        """Test searching resources by ESF."""
        # Setup test data - ESF and cost_period are pre-seeded
        user = create_test_user("searcher", "Resource Searcher", "password")
        resource = create_test_resource(
            "1234567890",
            "searcher",
            "Test Ambulance",
            "Ford",
            "33.7490",
            "-84.3880",
            1,
            "100.00",
            1,
        )

        insert_user_to_db(user)
        insert_resource_to_db(resource)

        # Login
        client.post("/login", data={"username": "searcher", "password": "password"})

        # Search by ESF
        response = client.post("/search-resources/", data={"esf": "1"})

        assert response.status_code == 200
        assert "Test Ambulance" in response.get_data(as_text=True)

    def test_search_resources_by_keyword(self, client, clean_db):
        """Test searching resources by keyword."""
        # Setup test data
        user = create_test_user("searcher", "Resource Searcher", "password")
        resource = create_test_resource(
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

        insert_user_to_db(user)
        insert_resource_to_db(resource)

        # Login
        client.post("/login", data={"username": "searcher", "password": "password"})

        # Search by keyword
        response = client.post("/search-resources/", data={"keyword": "Ambulance"})

        assert response.status_code == 200
        assert "Emergency Ambulance" in response.get_data(as_text=True)

    def test_search_resources_by_distance(self, client, clean_db):
        """Test searching resources by distance."""
        # Setup test data - ESF and cost_period are pre-seeded
        user = create_test_user("searcher", "Resource Searcher", "password")
        resource = create_test_resource(
            "1234567890",
            "searcher",
            "Test Ambulance",
            "Ford",
            "33.7490",
            "-84.3880",
            1,
            "100.00",
            1,
        )

        insert_user_to_db(user)
        insert_resource_to_db(resource)

        # Login
        client.post("/login", data={"username": "searcher", "password": "password"})

        # Search by distance
        response = client.post("/search-resources/", data={"distance": "50"})

        assert response.status_code == 200

    def test_resource_deployment_workflow(self, client, clean_db):
        """Test deploying a resource to an incident."""
        # Setup test data
        user = create_test_user("coordinator", "Emergency Coordinator", "password")
        resource = create_test_resource(
            "1234567890",
            "coordinator",
            "Test Ambulance",
            "Ford",
            "33.7490",
            "-84.3880",
            1,
            "100.00",
            1,
        )
        incident = create_test_incident(
            1, "coordinator", "Emergency Response", "Emergency", "33.7500", "-84.3890"
        )

        insert_user_to_db(user)
        insert_resource_to_db(resource)
        insert_incident_to_db(incident)

        # Login
        client.post("/login", data={"username": "coordinator", "password": "password"})

        # Deploy resource
        response = client.get("/search-resources/deploy/?resource-id=1234567890&incident-id=1")

        assert response.status_code == 302
        assert "/resource-status" in response.location

    def test_resource_request_workflow(self, client, clean_db):
        """Test requesting a resource for an incident."""
        # Setup test data
        user = create_test_user("coordinator", "Emergency Coordinator", "password")
        resource = create_test_resource(
            "1234567890",
            "coordinator",
            "Test Ambulance",
            "Ford",
            "33.7490",
            "-84.3880",
            1,
            "100.00",
            1,
        )
        incident = create_test_incident(
            1, "coordinator", "Emergency Response", "Emergency", "33.7500", "-84.3890"
        )

        insert_user_to_db(user)
        insert_resource_to_db(resource)
        insert_incident_to_db(incident)

        # Login
        client.post("/login", data={"username": "coordinator", "password": "password"})

        # Request resource
        response = client.get("/search-resources/request/?resource-id=1234567890&incident-id=1")

        assert response.status_code == 302
        assert "/resource-status" in response.location

    def test_resource_repair_workflow(self, client, clean_db):
        """Test requesting resource repair."""
        # Setup test data
        user = create_test_user("owner", "Resource Owner", "password")
        resource = create_test_resource(
            "1234567890", "owner", "Test Ambulance", "Ford", "33.7490", "-84.3880", 1, "100.00", 1
        )

        insert_user_to_db(user)
        insert_resource_to_db(resource)

        # Login
        client.post("/login", data={"username": "owner", "password": "password"})

        # Request repair
        response = client.get("/search-resources/repair/?resource-id=1234567890")

        assert response.status_code == 302
        assert "/resource-status" in response.location

    def test_complete_resource_lifecycle(self, client, clean_db):
        """Test complete workflow: Add → Search → Deploy → Check Status."""
        # Setup test data
        user = create_test_user("coordinator", "Emergency Coordinator", "password")
        incident = create_test_incident(
            1, "coordinator", "Emergency Response", "Emergency", "33.7500", "-84.3890"
        )

        insert_user_to_db(user)
        insert_incident_to_db(incident)

        # Login
        client.post("/login", data={"username": "coordinator", "password": "password"})

        # Step 1: Add resource
        response = client.post(
            "/add-resource/",
            data={
                "submit": "Add Resource",
                "resource_id": "1234567890",
                "name": "Emergency Ambulance",
                "model": "Ford",
                "lat": "33.7490",
                "long": "-84.3880",
                "cost": "100.00",
                "esf_id": "1",
                "cost_id": "1",
            },
        )
        assert response.status_code == 302

        # Step 2: Search for resource
        response = client.post("/search-resources/", data={"esf": "1"}, follow_redirects=True)
        assert response.status_code == 200
        assert "Emergency Ambulance" in response.get_data(as_text=True)

        # Step 3: Deploy resource
        response = client.get("/search-resources/deploy/?resource-id=1234567890&incident-id=1")
        assert response.status_code == 302

        # Step 4: Check resource status
        response = client.get("/resource-status/")
        assert response.status_code == 200
