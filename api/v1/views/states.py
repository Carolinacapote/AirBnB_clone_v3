#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort
from flask import jsonify
from flask import request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<id>', methods=['GET'], strict_slashes=False)
def get_states(id=None):
    """ def get_states(Retrieves the list of all State objects) """
    if id is None:
        states = storage.all(storage.classes['State'])
        return jsonify([obj.to_dict() for obj in states.values()])

    else:
        state = storage.get(storage.classes['State'], id)
        if state is None:
            abort(404)
        return state.to_dict(), 200


@app_views.route('/states/<id>', methods=['DELETE'], strict_slashes=False)
def delete_state(id):
    """ Deletes a State object """
    state = storage.get(storage.classes['State'], id)
    if state is None:
        abort(404)

    state.delete()
    storage.save()
    return {}, 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a State object """
    try:
        data = request.get_json()
    except Exception as err:
        abort(400, 'Not a JSON')

    if 'name' in data.keys():
        new_state = State(name=data.get('name'))
        new_state.save()
        return new_state.to_dict(), 201

    abort(400, 'Missing name')


@app_views.route('/states/<id>', methods=['PUT'], strict_slashes=False)
def update_state(id):
    """ Updates a State object """
    try:
        data = request.get_json()
    except Exception as err:
        abort(400, 'Not a JSON')

    state = storage.get(storage.classes['State'], id)
    if state is None:
        abort(404)

    if 'name' in data.keys():
        setattr(state, 'name', data.get('name'))
        state.save()

    return state.to_dict(), 200
