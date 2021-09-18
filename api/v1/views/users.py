#!/usr/bin/python3
"""
declare the veiws for users
"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort
from flask import jsonify
from flask import request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<id>', methods=['GET'], strict_slashes=False)
def get_users(id=None):
    """ Retrieves the list of all Users objects or a user object by Id """
    if id is None:
        users = storage.all(storage.classes['User'])
        return jsonify([obj.to_dict() for obj in users.values()])

    else:
        user = storage.get(storage.classes['User'], id)
        if user is None:
            abort(404)
        return user.to_dict(), 200


@app_views.route('/users/<id>', methods=['DELETE'], strict_slashes=False)
def delete_user(id):
    """ Deletes a User object """
    user = storage.get(storage.classes['User'], id)
    if user is None:
        abort(404)

    user.delete()
    storage.save()
    return {}, 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a User object """
    try:
        data = request.get_json()
    except Exception as err:
        abort(400, 'Not a JSON')

    if 'email' not in data.keys():
        abort(400, 'Missing email')

    if 'password' not in data.keys():
        abort(400, 'Missing password')

    new_user = User()
    for key, attr in data.items():
        if key not in ['id']:
            setattr(new_user, key, attr)

    new_user.save()
    return new_user.to_dict(), 201


@app_views.route('/users/<id>', methods=['PUT'], strict_slashes=False)
def update_user(id):
    """ Updates a User object """
    try:
        data = request.get_json()
    except Exception as err:
        abort(400, 'Not a JSON')

    user = storage.get(storage.classes['User'], id)
    if user is None:
        abort(404)

    for key, attr in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, attr)
    user.save()

    return user.to_dict(), 200
