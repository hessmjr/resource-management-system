
import bcrypt
from database import query_db
from flask import Blueprint, Response, redirect, render_template, request, session, url_for

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login() -> str | Response:
    error = None

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            error = 'Username and password are required'
        else:
            user = query_db("SELECT * FROM user WHERE username = %s", (username,))

            if user is None or len(user) < 1:
                error = 'Invalid username'
            elif not _verify_password(password, user[0][2]):
                error = 'Invalid password'
            else:
                session['username'] = user[0][0]
                session['name'] = user[0][1]
                return redirect(url_for('menu.menu'))

    return render_template('login.html', error=error)


@auth_bp.route('/logout')
def logout() -> Response:
    session.clear()
    return redirect(url_for('auth.login'))


def _verify_password(password: str, hashed_password: str) -> bool:
    # Supports both bcrypt hashes and legacy plaintext passwords
    if hashed_password.startswith('$2b$'):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    else:
        return password == hashed_password
