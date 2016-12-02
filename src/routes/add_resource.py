from re import compile, match
from string import Template
from uuid import uuid4

from flask import render_template, request, session, redirect, url_for, abort

from src.database import query_db, commit_db


def add_resource_route(error=None):
    """
    Adds a new resource to the system
    :return: template after user decision
    """
    # get all ESF's
    esfs = query_db("SELECT * FROM esf")

    # get all cost types
    costs = query_db("SELECT * FROM cost_time_period")

    # # get user's name
    owner_name = session.get('name')
    username = session.get('username')

    # create resource id
    resource_id = int(uuid4().int / 10.0**29)

    # build new resource form for user
    if request.method == 'GET':

        # return template to user
        return render_template('add_resource.html', resource_id=resource_id,
                               owner_name=owner_name, esfs=esfs,
                               cost_types=costs)

    # input from the user's form
    elif request.method == 'POST':

        # check if user submitted and try to submit new resource
        if 'submit' in request.form:
            error = add_rsrce(username, esfs, costs)

        # if user canceled or there is no error return to menu
        if 'cancel' in request.form or not error:
            return redirect(url_for('menu'))

        # pull resource id from the form if exists
        if 'resource_id' in request.form:
            resource_id = request.form['resource_id']

        # try again and let user know error
        return render_template('add_resource.html', resource_id=resource_id,
                               owner_name=owner_name, esfs=esfs,
                               cost_types=costs, error=error), 400

    # send user back to when complete
    return abort(405)


def add_rsrce(username, esfs, costs):
    """
    Validates all user submitted items and then attempts to insert info
    into database.  If anything fails it returns false bool and user must
    submit form again.
    :param username: current username
    :param esfs: list of valid esfs
    :param costs: list of valid cost types
    :return: bool
    """
    # check all user input values exist
    if 'resource_id' not in request.form or 'esf_id' not in request.form or \
            'cost_id' not in request.form or 'lat' not in request.form or \
            'long' not in request.form or 'cost' not in request.form or \
            'model' not in request.form or 'name' not in request.form:
        return "Form not filled out correctly"

    # get all user input values
    resource_id = request.form['resource_id']
    name = request.form['name']
    esf_id = request.form['esf_id']
    cost_id = request.form['cost_id']
    cost = request.form['cost']
    lat = request.form['lat']
    lng = request.form['long']
    model = request.form['model']

    # validate main esf
    if not validate_esf(esf_id, esfs):
        return "Invalid Primary ESF"
    if esf_id in request.form.getlist('second_esfs'):
        return "Duplicate primary and secondary ESF"
    esf_id = int(esf_id)

    # validate cost id
    if not validate_cost(cost_id, costs):
        return "Invalid cost type"
    cost_id = int(cost_id)

    # validate lat and long
    lat_regex = compile('^-?([1-8]?[1-9]|[1-9]0)\.\d{1,6}$')
    long_regex = compile('^-?(1[1-8][1-9]|[0-9]{1,2})\.\d{1,6}$')
    if not match(long_regex, lng) or not match(lat_regex, lat):
        return "Invalid latitude/longitude format"

    # validate cost
    cost_regex = compile('[\d]+(\.[\d]{2})?')
    if not match(cost_regex, cost):
        return "Invalid cost format"

    if float(cost) < 0.0:
        return "Cost amount negative"

    # validate the model
    model_regex = compile('[\w -.]+')
    if not match(model_regex, model):
        return "Model is not a valid format"

    # insert resource into db
    commit_db(new_resource_sql(resource_id, username, name, model, lat, lng,
                               cost_id, cost, esf_id))

    # validate each capability and insert, if any
    for cap in request.form.getlist('capabilities'):
        # only validated capabilities will get inserted
        if match(model_regex, cap):
            commit_db(add_capability_sql(resource_id, cap))

    # insert secondary esf into db
    for esf2 in request.form.getlist('second_esfs'):

        if validate_esf(esf2, esfs):
            commit_db(add_sec_esf_sql(resource_id, esf2))

    # return result
    return None


def validate_cost(cost_id, costs):
    """
    Validates a cost param
    :param cost_id: cost ID to be validated
    :param costs: list of costs to validate against
    :return: bool
    """
    # ensure id is a digit first
    if not unicode.isdigit(cost_id):
        return False

    # convert to integer
    cost_id = int(cost_id)

    # check if in valid cost types
    for cost in costs:
        if cost_id in cost:
            return True

    return False


def validate_esf(esf_id, esfs):
    """
    Validates a esf param
    :param esf_id: esf ID to be validated
    :param esfs: list of costs to validate against
    :return: bool
    """
    # ensure id is a digit first
    if not unicode.isdigit(esf_id):
        return False

    # convert to integer
    esf_id = int(esf_id)

    # check if in valid esfs
    for esf in esfs:
        if esf_id in esf:
            return True

    return False


def new_resource_sql(resource_id, username, name, model, lat, longitude,
                     cost_id, amount, esf_id):
    """
    Builds new resource SQL
    """
    t = Template("""
        INSERT INTO resource
        VALUES ('$guid', '$cost_id', '$username', '$resource_name',
            '$model', '$lat', '$long', '$amount', '$esf_id')
    """)

    return t.safe_substitute({'username': username, 'guid': resource_id,
                              'resource_name': name, 'model': model,
                              'lat': lat, 'long': longitude, 'cost_id': cost_id,
                              'amount': amount, 'esf_id': esf_id})


def add_sec_esf_sql(resource_id, second_esf_id):
    """
    Builds SQL for adding new secondary esfs
    """
    t = Template("""
        INSERT INTO resource_esf
        VALUES ('$guid', '$esf_id')
    """)

    return t.safe_substitute({'guid': resource_id, 'esf_id': second_esf_id})


def add_capability_sql(resource_id, capability):
    """
    Builds SQL for adding capabilities for a resource
    :return: String SQL Query
    """
    t = Template("""
        INSERT INTO capability
        VALUES ('$guid', '$capability')
    """)

    return t.safe_substitute({'guid': resource_id, 'capability': capability})
