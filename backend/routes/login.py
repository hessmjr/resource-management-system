from typing import Union
from flask import render_template, request, url_for, redirect, session, Response
import bcrypt

from database import query_db


def index_route() -> Union[str, Response]:
    """
    Method for handling user login
    :return: rendered template or redirect response
    """
    error = None

    # handle user logging in
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            error = 'Username and password are required'
        else:
            # query the db for the user information using parameterized query
            user = query_db("SELECT * FROM user WHERE username = %s", (username,))

            # ensure user exists in database first
            if user is None or len(user) < 1:
                error = 'Invalid username'

            # if user does exist check password hash
            elif not _verify_password(password, user[0][2]):
                error = 'Invalid password'

            # if user exists and password checks then send to main menu
            else:
                session['username'] = user[0][0]
                session['name'] = user[0][1]
                return redirect(url_for('main.menu'))

    # give user login html
    return render_template('login.html', error=error)


def _verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    Supports both bcrypt hashes and legacy plaintext passwords.
    :param password: Plain text password
    :param hashed_password: Stored password hash or plaintext
    :return: True if password matches
    """
    # Check if it's a bcrypt hash (starts with $2b$)
    if hashed_password.startswith('$2b$'):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    else:
        # Legacy plaintext comparison (for backward compatibility)
        return password == hashed_password
