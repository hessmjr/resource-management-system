"""
Test data helpers for creating and inserting test data.
Each test creates its own data dynamically.
"""

from database import commit_db


def create_test_user(username: str, name: str, password: str) -> dict:
    """Create test user data."""
    return {"username": username, "name": name, "password": password}


def insert_user_to_db(user: dict) -> None:
    """Insert user into database."""
    commit_db(
        "INSERT INTO user VALUES (%s, %s, %s)", (user["username"], user["name"], user["password"])
    )


def create_test_esf(esf_id: int, description: str) -> dict:
    """Create test ESF data."""
    return {"esf_id": esf_id, "description": description}


def insert_esf_to_db(esf: dict) -> None:
    """Insert ESF into database."""
    commit_db("INSERT INTO esf VALUES (%s, %s)", (esf["esf_id"], esf["description"]))


def create_test_cost_period(cost_id: int, description: str) -> dict:
    """Create test cost time period data."""
    return {"cost_time_period_id": cost_id, "description": description}


def insert_cost_period_to_db(cost_period: dict) -> None:
    """Insert cost time period into database."""
    commit_db(
        "INSERT INTO cost_time_period VALUES (%s, %s)",
        (cost_period["cost_time_period_id"], cost_period["description"]),
    )


def create_test_incident(
    incident_id: int,
    username: str,
    description: str,
    incident_type: str,
    latitude: str,
    longitude: str,
) -> dict:
    """Create test incident data."""
    return {
        "incident_id": incident_id,
        "username": username,
        "description": description,
        "incident_type": incident_type,
        "latitude": latitude,
        "longitude": longitude,
    }


def insert_incident_to_db(incident: dict) -> None:
    """Insert incident into database."""
    commit_db(
        """INSERT INTO incident VALUES (%s, %s, %s, %s, %s, %s)""",
        (
            incident["incident_id"],
            incident["username"],
            incident["description"],
            incident["incident_type"],
            incident["latitude"],
            incident["longitude"],
        ),
    )


def create_test_resource(
    resource_id: str,
    username: str,
    name: str,
    model: str,
    latitude: str,
    longitude: str,
    cost_id: int,
    amount: str,
    esf_id: int,
) -> dict:
    """Create test resource data."""
    return {
        "resource_id": resource_id,
        "cost_time_period_id": cost_id,
        "username": username,
        "name": name,
        "model": model,
        "latitude": latitude,
        "longitude": longitude,
        "amount": amount,
        "primary_esf_id": esf_id,
    }


def insert_resource_to_db(resource: dict) -> None:
    """Insert resource into database."""
    commit_db(
        """INSERT INTO resource VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            resource["resource_id"],
            resource["cost_time_period_id"],
            resource["username"],
            resource["name"],
            resource["model"],
            resource["latitude"],
            resource["longitude"],
            resource["amount"],
            resource["primary_esf_id"],
        ),
    )


def create_test_capability(resource_id: str, capability: str) -> dict:
    """Create test capability data."""
    return {"resource_id": resource_id, "capability": capability}


def insert_capability_to_db(capability: dict) -> None:
    """Insert capability into database."""
    commit_db(
        "INSERT INTO capability VALUES (%s, %s)",
        (capability["resource_id"], capability["capability"]),
    )


def create_test_resource_esf(resource_id: str, esf_id: int) -> dict:
    """Create test resource ESF data."""
    return {"resource_id": resource_id, "esf_id": esf_id}


def insert_resource_esf_to_db(resource_esf: dict) -> None:
    """Insert resource ESF into database."""
    commit_db(
        "INSERT INTO resource_esf VALUES (%s, %s)",
        (resource_esf["resource_id"], resource_esf["esf_id"]),
    )
