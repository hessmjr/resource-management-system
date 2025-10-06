"""Main API routes for the ERMS backend."""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from ..services.user_service import UserService
from ..services.resource_service import ResourceService
from ..services.incident_service import IncidentService

bp = Blueprint('api', __name__)


@bp.route('/menu')
def menu():
    """Display user menu with user details."""
    username = session.get('username')
    if not username:
        return redirect(url_for('auth.login'))
    
    details = UserService.get_user_details(username)
    return render_template("menu.html", details=details)


@bp.route('/add-resource', methods=['GET', 'POST'])
def add_resource():
    """Handle adding new resources."""
    username = session.get('username')
    if not username:
        return redirect(url_for('auth.login'))
    
    # Get form data
    esfs = ResourceService.get_all_esfs()
    costs = ResourceService.get_all_cost_types()
    owner_name = session.get('name')
    
    if request.method == 'GET':
        return render_template('add_resource.html', 
                             owner_name=owner_name, 
                             esfs=esfs, 
                             cost_types=costs)
    
    elif request.method == 'POST':
        if 'cancel' in request.form:
            return redirect(url_for('api.menu'))
        
        if 'submit' in request.form:
            error = _validate_and_create_resource(request.form, esfs, costs, username)
            
            if not error:
                flash('Resource successfully created.')
                return redirect(url_for('api.menu'))
            
            return render_template('add_resource.html', 
                                 owner_name=owner_name, 
                                 esfs=esfs, 
                                 cost_types=costs, 
                                 error=error), 400
    
    return abort(405)


@bp.route('/search-resources', methods=['GET', 'POST'])
def search_resources():
    """Handle resource search."""
    username = session.get('username')
    if not username:
        return redirect(url_for('auth.login'))
    
    esfs = ResourceService.get_all_esfs()
    incidents = IncidentService.get_user_incidents(username)
    
    if request.method == 'GET':
        return render_template('search_resources.html', 
                             esfs=esfs, 
                             incidents=incidents)
    
    elif request.method == 'POST':
        if 'cancel' in request.form:
            return redirect(url_for('api.menu'))
        
        # Extract search parameters
        search_params = {
            'keyword': request.form.get('keyword', ''),
            'esf_id': request.form.get('esf', ''),
            'incident_id': request.form.get('incident_id', ''),
            'distance': request.form.get('distance', '')
        }
        
        # Validate distance if provided
        if search_params['distance'] and not search_params['distance'].isdigit():
            error = "Distance value must be positive number"
            return render_template('search_resources.html', 
                                 esfs=esfs, 
                                 incidents=incidents, 
                                 error=error)
        
        # Perform search
        results = ResourceService.search_resources(search_params)
        
        # Get incident details if searching by incident
        incident = None
        if search_params['incident_id']:
            incident = IncidentService.get_incident_by_id(search_params['incident_id'])
        
        return render_template('search_results.html', 
                             username=username,
                             incident=incident, 
                             results=results)
    
    return abort(405)


def _validate_and_create_resource(form_data, esfs, costs, username):
    """Validate form data and create resource if valid."""
    # Check required fields
    required_fields = ['name', 'esf_id', 'cost_id', 'lat', 'long', 'cost', 'model']
    for field in required_fields:
        if field not in form_data or not form_data[field]:
            return "Form not filled out correctly"
    
    # Validate ESF
    if not ResourceService.validate_esf(form_data['esf_id'], esfs):
        return "Invalid Primary ESF"
    
    # Check for duplicate primary and secondary ESF
    secondary_esfs = form_data.getlist('second_esfs')
    if form_data['esf_id'] in secondary_esfs:
        return "Duplicate primary and secondary ESF"
    
    # Validate cost type
    if not ResourceService.validate_cost_type(form_data['cost_id'], costs):
        return "Invalid cost type"
    
    # Validate coordinates
    if not ResourceService.validate_coordinates(form_data['lat'], form_data['long']):
        return "Invalid latitude/longitude format"
    
    # Validate cost
    if not ResourceService.validate_cost(form_data['cost']):
        return "Invalid cost format"
    
    # Validate model
    if not ResourceService.validate_model(form_data['model']):
        return "Model is not a valid format"
    
    # Create resource data
    resource_data = {
        'username': username,
        'name': form_data['name'],
        'model': form_data['model'],
        'lat': form_data['lat'],
        'lng': form_data['long'],
        'cost_id': form_data['cost_id'],
        'cost': form_data['cost'],
        'esf_id': form_data['esf_id'],
        'secondary_esfs': secondary_esfs,
        'capabilities': form_data.getlist('capabilities')
    }
    
    try:
        ResourceService.create_resource(resource_data)
        return None
    except Exception as e:
        return f"Error creating resource: {str(e)}"