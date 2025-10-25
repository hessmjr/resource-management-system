from string import Template
from typing import Any

from database import commit_db, get_db, query_db


class ResourceDAL:
    def __init__(self):
        self.db = get_db()

    def get_all_esfs(self) -> list[tuple[Any, ...]]:
        return query_db("SELECT * FROM esf")

    def get_all_cost_types(self) -> list[tuple[Any, ...]]:
        return query_db("SELECT * FROM cost_time_period")

    def create_resource(self, resource_id: int, username: str, name: str, model: str,
                       lat: str, lng: str, cost_id: int, cost: str, esf_id: int) -> None:
        template = Template("""
            INSERT INTO resource
            VALUES ('$guid', '$cost_id', '$username', '$resource_name',
                '$model', '$lat', '$long', '$amount', '$esf_id')
        """)

        sql = template.safe_substitute({
            'username': username,
            'guid': resource_id,
            'resource_name': name,
            'model': model,
            'lat': lat,
            'long': lng,
            'cost_id': cost_id,
            'amount': cost,
            'esf_id': esf_id
        })
        commit_db(sql)

    def add_resource_capability(self, resource_id: int, capability: str) -> None:
        template = Template("""
            INSERT INTO capability
            VALUES ('$guid', '$capability')
        """)

        sql = template.safe_substitute({
            'guid': resource_id,
            'capability': capability
        })
        commit_db(sql)

    def add_secondary_esf(self, resource_id: int, esf_id: int) -> None:
        template = Template("""
            INSERT INTO resource_esf
            VALUES ('$guid', '$esf_id')
        """)

        sql = template.safe_substitute({
            'guid': resource_id,
            'esf_id': esf_id
        })
        commit_db(sql)
