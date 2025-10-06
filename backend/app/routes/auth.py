"""Authentication routes for the ERMS backend."""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..services.user_service import UserService

bp = Blueprint('auth', __name__)


@bp.route('/', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    error = None
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            error = 'Username and password are required'
        else:
            user = UserService.authenticate_user(username, password)
            
            if not user:
                error = 'Invalid username or password'
            else:
                session['username'] = user['username']
                session['name'] = user['name']
                return redirect(url_for('api.menu'))
    
    return render_template('login.html', error=error)


@bp.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    return redirect(url_for('auth.login'))