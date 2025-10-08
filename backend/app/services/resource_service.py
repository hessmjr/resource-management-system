"""Resource service for managing resource-related database operations."""

import re
from uuid import uuid4
from ..config import query_db, execute_db


class ResourceService:
    """Service class for resource-related operations."""
    
    @staticmethod
    def get_all_esfs():
        """Get all Emergency Support Functions."""
        return query_db("SELECT * FROM esf")
    
    @staticmethod
    def get_all_cost_types():
        """Get all cost time periods."""
        return query_db("SELECT * FROM cost_time_period")
    
    @staticmethod
    def validate_esf(esf_id, esfs):
        """Validate if ESF ID exists in the provided ESF list."""
        if not esf_id.isdigit():
            return False
        
        esf_id = int(esf_id)
        return any(esf_id in esf for esf in esfs)
    
    @staticmethod
    def validate_cost_type(cost_id, costs):
        """Validate if cost type ID exists in the provided cost list."""
        if not cost_id.isdigit():
            return False
        
        cost_id = int(cost_id)
        return any(cost_id in cost for cost in costs)
    
    @staticmethod
    def validate_coordinates(lat, lng):
        """Validate latitude and longitude values."""
        try:
            lat_f = float(lat)
            lng_f = float(lng)
        except (TypeError, ValueError):
            return False
        return -90.0 <= lat_f <= 90.0 and -180.0 <= lng_f <= 180.0
    
    @staticmethod
    def validate_cost(cost):
        """Validate cost format."""
        cost_regex = re.compile(r'[\d]+(\.[\d]{2})?')
        if not cost_regex.match(cost):
            return False
        return float(cost) >= 0.0
    
    @staticmethod
    def validate_model(model):
        """Validate model format."""
        model_regex = re.compile(r'[\w .-]+')
        return bool(model_regex.match(model))
    
    @staticmethod
    def create_resource(resource_data):
        """Create a new resource with validation."""
        username = resource_data['username']
        name = resource_data['name']
        model = resource_data['model']
        lat = resource_data['lat']
        lng = resource_data['lng']
        cost_id = resource_data['cost_id']
        cost = resource_data['cost']
        esf_id = resource_data['esf_id']
        secondary_esfs = resource_data.get('secondary_esfs', [])
        capabilities = resource_data.get('capabilities', [])
        
        # Generate resource ID
        resource_id = str(int(uuid4().int / 10.0**29))
        
        # Insert main resource
        resource_query = """
            INSERT INTO resource
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        execute_db(resource_query, (
            resource_id, cost_id, username, name, model, lat, lng, cost, esf_id
        ))
        
        # Insert secondary ESFs
        for esf in secondary_esfs:
            esf_query = "INSERT INTO resource_esf VALUES (%s, %s)"
            execute_db(esf_query, (resource_id, esf))
        
        # Insert capabilities
        for capability in capabilities:
            if ResourceService.validate_model(capability):  # Reuse model validation for capabilities
                capability_query = "INSERT INTO capability VALUES (%s, %s)"
                execute_db(capability_query, (resource_id, capability))
        
        return resource_id
    
    @staticmethod
    def search_resources(search_params):
        """Search resources based on various criteria."""
        keyword = search_params.get('keyword', '')
        esf_id = search_params.get('esf_id', '')
        incident_id = search_params.get('incident_id', '')
        distance = search_params.get('distance', '')
        
        # Build query based on search parameters
        if keyword and not esf_id and not incident_id:
            return ResourceService._keyword_search(keyword)
        elif esf_id and not keyword and not incident_id:
            return ResourceService._esf_search(esf_id)
        elif incident_id and not keyword and not esf_id:
            return ResourceService._incident_search(incident_id, distance)
        elif keyword and esf_id and not incident_id:
            return ResourceService._keyword_esf_search(keyword, esf_id)
        elif keyword and incident_id and not esf_id:
            return ResourceService._keyword_incident_search(keyword, incident_id, distance)
        elif esf_id and incident_id and not keyword:
            return ResourceService._incident_esf_search(esf_id, incident_id, distance)
        elif keyword and esf_id and incident_id:
            return ResourceService._all_criteria_search(keyword, esf_id, incident_id, distance)
        else:
            return ResourceService._no_criteria_search()
    
    @staticmethod
    def _keyword_search(keyword):
        """Search resources by keyword."""
        query = """
            SELECT DISTINCT resource.resource_id, resource.name, user.name,
                resource.amount, cost_time_period.time_period,
                requests.request_status, requests.return_by_date
            FROM resource
            LEFT JOIN capability
                ON resource.resource_id = capability.resource_id
            JOIN user
                ON resource.username = user.username
            JOIN cost_time_period
                ON cost_time_period.cost_time_period_id = resource.cost_time_period_id
            LEFT JOIN
                (SELECT resource_id, return_by_date,
                    CASE WHEN status = 'Deployed' or CURRENT_DATE < return_by_date
                        THEN 'Not Available'
                        ELSE 'Available'
                    END AS request_status
                FROM resource_request
                JOIN resource_request_status
                    ON resource_request_status.resource_request_status_id =
                        resource_request.resource_request_status_id
                GROUP BY resource_id
                ) requests
                    ON requests.resource_id = resource.resource_id
            WHERE resource.name LIKE %s OR
                resource.model LIKE %s OR
                capability.capability LIKE %s
            ORDER BY requests.request_status, resource.name
        """
        keyword_pattern = f'%{keyword}%'
        return query_db(query, (keyword_pattern, keyword_pattern, keyword_pattern))
    
    @staticmethod
    def _esf_search(esf_id):
        """Search resources by ESF."""
        query = """
            SELECT DISTINCT resource.resource_id, resource.name, user.name,
                resource.amount, cost_time_period.time_period,
                requests.request_status, requests.return_by_date
            FROM resource
            LEFT JOIN resource_esf
                ON resource.resource_id = resource_esf.resource_id
            JOIN user
                ON resource.username = user.username
            JOIN cost_time_period
                ON cost_time_period.cost_time_period_id = resource.cost_time_period_id
            LEFT JOIN
                (SELECT resource_id, return_by_date,
                    CASE WHEN status = 'Deployed' or CURRENT_DATE < return_by_date
                        THEN 'Not Available'
                        ELSE 'Available'
                    END AS request_status
                FROM resource_request
                JOIN resource_request_status
                    ON resource_request_status.resource_request_status_id =
                        resource_request.resource_request_status_id
                GROUP BY resource_id
                ) requests
                    ON requests.resource_id = resource.resource_id
            WHERE resource_esf.esf_id = %s OR resource.primary_esf_id = %s
            ORDER BY requests.request_status, resource.name
        """
        return query_db(query, (esf_id, esf_id))
    
    @staticmethod
    def _incident_search(incident_id, distance):
        """Search resources by incident location."""
        distance = ResourceService._convert_distance(distance)
        query = """
            SELECT DISTINCT resource.resource_id, resource.name, user.name,
                resource.amount, cost_time_period.time_period,
                requests.request_status, requests.return_by_date,
                distance_formula(resource.latitude, resource.longitude,
                    incident_info.latitude, incident_info.longitude) AS distance,
                resource.username
            FROM resource
            JOIN user
                ON resource.username = user.username
            JOIN cost_time_period
                ON cost_time_period.cost_time_period_id = resource.cost_time_period_id
            LEFT JOIN
                (SELECT resource_id, return_by_date,
                    CASE WHEN status = 'Deployed' or CURRENT_DATE < return_by_date
                        THEN 'Not Available'
                        ELSE 'Available'
                    END AS request_status
                FROM resource_request
                JOIN resource_request_status
                    ON resource_request_status.resource_request_status_id =
                        resource_request.resource_request_status_id
                GROUP BY resource_id
                ) requests
                    ON requests.resource_id = resource.resource_id
            CROSS JOIN
                (SELECT incident_id, latitude, longitude
                FROM incident
                WHERE incident_id = %s) incident_info
            WHERE distance_formula(resource.latitude, resource.longitude,
                incident_info.latitude, incident_info.longitude) < %s
            ORDER BY distance ASC, requests.request_status, resource.name
        """
        return query_db(query, (incident_id, distance))
    
    @staticmethod
    def _no_criteria_search():
        """Search all resources without criteria."""
        query = """
            SELECT DISTINCT resource.resource_id, resource.name, user.name,
                resource.amount, cost_time_period.time_period,
                requests.request_status, requests.return_by_date
            FROM resource
            JOIN user
                ON resource.username = user.username
            JOIN cost_time_period
                ON cost_time_period.cost_time_period_id = resource.cost_time_period_id
            LEFT JOIN
                (SELECT resource_id, return_by_date,
                    CASE WHEN status = 'Deployed' or CURRENT_DATE < return_by_date
                        THEN 'Not Available'
                        ELSE 'Available'
                    END AS request_status
                FROM resource_request
                JOIN resource_request_status
                    ON resource_request_status.resource_request_status_id =
                        resource_request.resource_request_status_id
                GROUP BY resource_id
                ) requests
                    ON requests.resource_id = resource.resource_id
        """
        return query_db(query)
    
    @staticmethod
    def _convert_distance(distance):
        """Convert distance string to float for database queries."""
        max_distance = 999999
        
        if not distance:
            return max_distance
        
        try:
            distance_value = float(distance)
        except (TypeError, ValueError):
            return max_distance
        
        delta = 0.000001
        
        if distance_value - delta < delta:
            return max_distance
        
        return distance_value
    
    # Additional search methods would be implemented similarly...
    @staticmethod
    def _keyword_esf_search(keyword, esf_id):
        """Search by keyword and ESF."""
        # Implementation similar to above methods
        pass
    
    @staticmethod
    def _keyword_incident_search(keyword, incident_id, distance):
        """Search by keyword and incident."""
        # Implementation similar to above methods
        pass
    
    @staticmethod
    def _incident_esf_search(esf_id, incident_id, distance):
        """Search by incident and ESF."""
        # Implementation similar to above methods
        pass
    
    @staticmethod
    def _all_criteria_search(keyword, esf_id, incident_id, distance):
        """Search by all criteria."""
        # Implementation similar to above methods
        pass