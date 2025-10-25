from datetime import datetime

from dal.resource_status_dal import ResourceStatusDAL
from flask import abort, redirect, render_template, request, session, url_for


class ResourceStatusService:
    """
    Service layer for Resource Status business logic.
    Handles resource status display and status updates.
    """

    def __init__(self):
        self.dal = ResourceStatusDAL()

    def get_resource_status_page(self, error=None):
        """
        Get the resource status page with all resource data.

        :param error: Any existing error message
        :return: rendered template
        """
        username = session.get("username")
        now = datetime.today().date()

        # query to get the statuses of user resources
        in_use = self.dal.get_resources_in_use(username)
        requested = self.dal.get_resources_requested(username)
        requests_received = self.dal.get_resource_requests_received(username)
        repairs = self.dal.get_resources_in_repair(username)

        # return rendered template to user with any errors
        return render_template(
            "resource_status.html",
            resources_in_use=in_use,
            resources_requested=requested,
            resource_requests_received=requests_received,
            resource_repairs=repairs,
            now=now,
            error=error,
        )

    def update_resource_status(self):
        """
        Updates the database with the given SQL statement.

        :return: redirect to resource status page
        """
        # get requested resource ID
        req_id = request.args.get("id", "")

        # determine which action to take based on URL
        action = self._determine_action_from_url()

        if action is None:
            abort(405)

        # if ID isn't blank create query and update database
        if req_id != "":
            self.dal.update_resource_status(action, req_id)

        return redirect(url_for("resource_status.resource_status"))

    def _determine_action_from_url(self):
        """
        Determine the action to take based on the current URL.

        :return: action string or None if invalid
        """
        url = request.url

        if "/deploy" in url:
            return "deploy"
        elif "/return" in url:
            return "return"
        elif "/reject" in url:
            return "reject"
        elif "/request/cancel" in url:
            return "cancel_request"
        elif "/repair/cancel" in url:
            return "cancel_repair"

        return None
