from uuid import uuid4

from dal.add_incident_dal import AddIncidentDAL
from flask import abort, flash, redirect, render_template, request, session, url_for
from utils.validators import validate_coordinates


class AddIncidentService:
    """
    Service layer for Add Incident business logic.
    Handles incident creation and validation.
    """

    def __init__(self):
        self.dal = AddIncidentDAL()

    def handle_add_incident_request(self, error=None):
        """
        Handles the add incident request (GET and POST).

        :param error: Any existing error message
        :return: rendered template or redirect
        """
        # get owner and create ID
        username = session.get('username')
        incident_id = int(uuid4().int / 10.0**29)

        if request.method == 'GET':
            return self._show_add_incident_form(incident_id, error)

        elif request.method == 'POST':
            return self._process_add_incident_form(incident_id, username, error)

        return abort(405)

    def _show_add_incident_form(self, incident_id, error):
        """Show the add incident form."""
        return render_template('add_incident.html',
                             incident_id=incident_id,
                             error=error)

    def _process_add_incident_form(self, incident_id, username, error):
        """Process the submitted add incident form."""
        if 'Save' in request.form:
            error = self._create_incident(username)

            if not error:
                flash('Incident successfully created.')

        if 'Cancel' in request.form or not error:
            return redirect(url_for('menu.index'))

        # Get incident_id from form if it exists
        if 'incident_id' in request.form:
            incident_id = request.form['incident_id']

        return render_template('add_incident.html',
                             incident_id=incident_id,
                             error=error), 400

    def _create_incident(self, username):
        """
        Validates and creates a new incident.

        :param username: Owner's username
        :return: error message if validation fails, None if successful
        """
        # Validate required fields
        validation_error = self._validate_required_fields()
        if validation_error:
            return validation_error

        # Extract form data
        form_data = self._extract_form_data()

        # Validate form data
        validation_error = self._validate_form_data(form_data)
        if validation_error:
            return validation_error

        # Create incident in database
        self.dal.create_incident(form_data, username)

        return None

    def _validate_required_fields(self):
        """Validate that all required fields are present."""
        required_fields = ['incident_id', 'lat', 'long', 'date']

        for field in required_fields:
            if field not in request.form:
                return "Missing parameter to add incident"

        return None

    def _extract_form_data(self):
        """Extract and return form data."""
        return {
            'incident_id': request.form['incident_id'],
            'description': request.form.get('description', ''),
            'date': request.form['date'],
            'lat': request.form['lat'],
            'lng': request.form['long']
        }

    def _validate_form_data(self, form_data):
        """Validate all form data."""
        # Validate coordinates
        if not validate_coordinates(form_data['lat'], form_data['lng']):
            return "Invalid latitude/longitude format"

        # Validate incident date
        try:
            from datetime import datetime
            datetime.strptime(form_data['date'], '%Y-%m-%d')
        except ValueError:
            return "Invalid incident date format. Please input YYYY-MM-DD"

        return None
