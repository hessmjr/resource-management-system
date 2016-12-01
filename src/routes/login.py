from flask import render_template, request, url_for, redirect, session

from src.database import query_db


def index_route():
    """
    Method for handling user login
    :return: rendered template
    """
    error = None

    # handle user logging in
    if request.method == 'POST':
        # query the db for the user information
        user = query_db("Select * FROM user WHERE username = '" +
                        request.form['username'] + "'")

        # ensure user exists in database first
        if user is None or len(user) < 1:
            error = 'Invalid username'

        # if user does exist check password hash
        elif not user[0][2] == request.form['password']:
            error = 'Invalid password'

        # if user exists and password checks then send to main menu
        else:
            session['username'] = user[0][0]
            session['name'] = user[0][1]
            return redirect(url_for('menu'))

    # give user login html
    return render_template('login.html', error=error)
