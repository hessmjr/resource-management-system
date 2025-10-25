from dal.search_resources_dal import SearchResourcesDAL
from flask import abort, redirect, render_template, request, session, url_for


class SearchResourcesService:
    """
    Service layer for Search Resources business logic.
    Handles resource search functionality and result actions.
    """

    def __init__(self):
        self.dal = SearchResourcesDAL()

    def handle_search_resources_request(self, error=None):
        """
        Handles the search resources request (GET and POST).

        :param error: Any existing error message
        :return: rendered template or redirect
        """
        username = session.get("username")

        # get all ESF's and incidents
        esfs = self.dal.get_all_esfs()
        incidents = self.dal.get_user_incidents(username)

        if request.method == "GET":
            return self._show_search_form(esfs, incidents, error)

        elif request.method == "POST":
            return self._process_search_request(esfs, incidents, username)

        return abort(405)

    def _show_search_form(self, esfs, incidents, error):
        """Show the search resources form."""
        return render_template("search_resources.html", esfs=esfs, incidents=incidents, error=error)

    def _process_search_request(self, esfs, incidents, username):
        """Process the search request."""
        # if user cancels then return to menu
        if "cancel" in request.form:
            return redirect(url_for("menu.index"))

        # extract search parameters
        search_params = self._extract_search_parameters()

        # validate search parameters
        validation_error = self._validate_search_parameters(search_params)
        if validation_error:
            return render_template(
                "search_resources.html", esfs=esfs, incidents=incidents, error=validation_error
            )

        # perform search
        results, incident = self.dal.search_resources(search_params)

        # render results
        return render_template(
            "search_results.html", username=username, incident=incident, results=results
        )

    def _extract_search_parameters(self):
        """Extract search parameters from form."""
        return {
            "esf_id": request.form.get("esf", ""),
            "keyword": request.form.get("keyword", ""),
            "distance": request.form.get("distance", ""),
            "incident_id": request.form.get("incident_id", ""),
        }

    def _validate_search_parameters(self, params):
        """Validate search parameters."""
        # check if distance value is valid
        if len(params["distance"]) > 0:
            if not params["distance"].isdigit():
                return "Distance value must be positive number"

        return None

    def handle_resource_request(self):
        """
        Handle resource request from search results.

        :return: redirect to resource status page
        """
        resource_id = request.args.get("resource-id")
        incident_id = request.args.get("incident-id")

        self.dal.create_resource_request(resource_id, incident_id)
        return redirect(url_for("resource_status.resource_status"))

    def handle_resource_deploy(self):
        """
        Handle resource deploy from search results.

        :return: redirect to resource status page
        """
        resource_id = request.args.get("resource-id")
        incident_id = request.args.get("incident-id")

        self.dal.create_resource_deploy(resource_id, incident_id)
        return redirect(url_for("resource_status.resource_status"))

    def handle_resource_repair(self):
        """
        Handle resource repair from search results.

        :return: redirect to resource status page
        """
        resource_id = request.args.get("resource-id")

        self.dal.create_resource_repair(resource_id)
        return redirect(url_for("resource_status.resource_status"))
