from uuid import uuid4

from dal.resource_dal import ResourceDAL
from flask import abort, flash, redirect, render_template, request, session, url_for
from utils.validators import (
    validate_capability_format,
    validate_coordinates,
    validate_cost_amount,
    validate_cost_format,
    validate_cost_id,
    validate_esf_id,
    validate_model_format,
)


class ResourceService:
    def __init__(self):
        self.dal = ResourceDAL()

    def handle_add_resource_request(self, error=None):
        esfs = self.dal.get_all_esfs()
        costs = self.dal.get_all_cost_types()
        owner_name = session.get("name")

        resource_id = int(uuid4().int / 10.0**29)

        if request.method == "GET":
            return self._show_add_resource_form(resource_id, owner_name, esfs, costs)

        elif request.method == "POST":
            return self._process_add_resource_form(resource_id, owner_name, esfs, costs, error)

        return abort(405)

    def _show_add_resource_form(self, resource_id, owner_name, esfs, costs):
        return render_template(
            "add_resource.html",
            resource_id=resource_id,
            owner_name=owner_name,
            esfs=esfs,
            cost_types=costs,
        )

    def _process_add_resource_form(self, resource_id, owner_name, esfs, costs, error):
        if "submit" in request.form:
            error = self._create_resource(username=session.get("username"), esfs=esfs, costs=costs)

            if not error:
                flash("Resource successfully created.")

        if "cancel" in request.form or not error:
            return redirect(url_for("menu.index"))

        if "resource_id" in request.form:
            resource_id = request.form["resource_id"]

        return render_template(
            "add_resource.html",
            resource_id=resource_id,
            owner_name=owner_name,
            esfs=esfs,
            cost_types=costs,
            error=error,
        ), 400

    def _create_resource(self, username, esfs, costs):
        validation_error = self._validate_required_fields()
        if validation_error:
            return validation_error

        form_data = self._extract_form_data()

        validation_error = self._validate_form_data(form_data, esfs, costs)
        if validation_error:
            return validation_error

        self._insert_resource_to_database(form_data, username)

        return None

    def _validate_required_fields(self):
        required_fields = [
            "resource_id",
            "esf_id",
            "cost_id",
            "lat",
            "long",
            "cost",
            "model",
            "name",
        ]

        for field in required_fields:
            if field not in request.form:
                return "Form not filled out correctly"

        return None

    def _extract_form_data(self):
        return {
            "resource_id": request.form["resource_id"],
            "name": request.form["name"],
            "esf_id": request.form["esf_id"],
            "cost_id": request.form["cost_id"],
            "cost": request.form["cost"],
            "lat": request.form["lat"],
            "lng": request.form["long"],
            "model": request.form["model"],
            "capabilities": request.form.getlist("capabilities"),
            "secondary_esfs": request.form.getlist("second_esfs"),
        }

    def _validate_form_data(self, form_data, esfs, costs):
        if not validate_esf_id(form_data["esf_id"], esfs):
            return "Invalid Primary ESF"

        if form_data["esf_id"] in form_data["secondary_esfs"]:
            return "Duplicate primary and secondary ESF"

        if not validate_cost_id(form_data["cost_id"], costs):
            return "Invalid cost type"

        if not validate_coordinates(form_data["lat"], form_data["lng"]):
            return "Invalid latitude/longitude format"

        if not validate_cost_format(form_data["cost"]):
            return "Invalid cost format"

        if not validate_cost_amount(form_data["cost"]):
            return "Cost amount negative"

        if not validate_model_format(form_data["model"]):
            return "Model is not a valid format"

        return None

    def _insert_resource_to_database(self, form_data, username):
        resource_id = int(form_data["resource_id"])
        esf_id = int(form_data["esf_id"])
        cost_id = int(form_data["cost_id"])

        self.dal.create_resource(
            resource_id=resource_id,
            username=username,
            name=form_data["name"],
            model=form_data["model"],
            lat=form_data["lat"],
            lng=form_data["lng"],
            cost_id=cost_id,
            cost=form_data["cost"],
            esf_id=esf_id,
        )

        for capability in form_data["capabilities"]:
            if validate_capability_format(capability):
                self.dal.add_resource_capability(resource_id, capability)

        for secondary_esf in form_data["secondary_esfs"]:
            if validate_esf_id(secondary_esf, self.dal.get_all_esfs()):
                self.dal.add_secondary_esf(resource_id, int(secondary_esf))
