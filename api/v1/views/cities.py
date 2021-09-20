#!/usr/bin/python3
"""
Script that starts a Flask Blueprint
"""
from api.v1.views import app_views
from models import storage
from models.city import City
from flask import abort
from flask import jsonify
from flask import request


@app_views.route('/cities/<id>', methods=['GET'], strict_slashes=False)
def get_city(id=None):
    """ Method that retrieves a city by id """
    city = storage.get(storage.classes['City'], id)
    if city is None:
        abort(404)
    return city.to_dict(), 200


@app_views.route('/states/<id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(id):
    """ Retrieves the list of all cities of a specific State """
    state = storage.get(storage.classes['State'], id)
    if state is None:
        abort(404)
    cities = state.cities

    return jsonify([obj.to_dict() for obj in cities])


@app_views.route('/cities/<id>', methods=['DELETE'], strict_slashes=False)
def delete_city(id):
    """ Deletes a City object """
    city = storage.get(storage.classes['City'], id)
    if city is None:
        abort(404)

    city.delete()
    storage.save()
    return {}, 200


@app_views.route('/states/<id>/cities', methods=['POST'], strict_slashes=False)
def create_city(id):
    """ Creates a City object """
    state = storage.get(storage.classes['State'], id)
    if state is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    if 'name' in data.keys():
        new_city = City(name=data.get('name'), state_id=id)
        new_city.save()
        return new_city.to_dict(), 201

    abort(400, 'Missing name')


@app_views.route('/cities/<id>', methods=['PUT'], strict_slashes=False)
def update_city(id):
    """ Updates a City object """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    city = storage.get(storage.classes['City'], id)
    if city is None:
        abort(404)

    if 'name' in data.keys():
        setattr(city, 'name', data.get('name'))
        city.save()

    return city.to_dict(), 200
