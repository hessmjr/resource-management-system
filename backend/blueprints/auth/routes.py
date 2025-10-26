"""
Authentication blueprint for handling login/logout routes.
"""

from flask import Blueprint, Response, redirect, render_template, request, url_for
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    """Handle login requests."""
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        service = AuthService()
        error = service.authenticate_user(username, password)

        if error is None:
            return redirect(url_for("menu.index"))

    return render_template("login.html", error=error)


@auth_bp.route("/logout")
def logout() -> Response:
    """Handle logout requests."""
    service = AuthService()
    service.logout_user()
    return redirect(url_for("auth.login"))
