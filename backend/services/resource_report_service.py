from dal.resource_report_dal import ResourceReportDAL
from flask import render_template, session


class ResourceReportService:
    """
    Service layer for Resource Report business logic.
    Handles resource reporting functionality.
    """

    def __init__(self):
        self.dal = ResourceReportDAL()

    def handle_resource_report_request(self):
        """
        Handle the resource report request.

        :return: rendered template
        """
        username = session.get("username")

        # query database for report information
        results = self.dal.get_resource_report(username)

        return render_template("resource_report.html", results=results)
