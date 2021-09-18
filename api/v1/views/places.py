#!/usr/bin/python3
"""
Script that starts a Flask Blueprint
"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from flask import abort
from flask import jsonify
from flask import request


@app_views.route('/cities/<id>/places', methods=['GET'], strict_slashes=False)
def get_places(id=None):
    """ Method that retrieves a list of all places of a City """
    city = storage.get(storage.classes['City'], id)
    if city is None:
        abort(404)
    places = city.places

    return jsonify([obj.to_dict() for obj in places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """ Method that retrieves a list of all places of a City """
    place = storage.get(storage.classes['Place'], place_id)
    if place is None:
        abort(404)

    return place.to_dict(), 200


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place = storage.get(storage.classes['Place'], place_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()
    return {}, 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ Creates a Place object """
    city = storage.get(storage.classes['City'], city_id)
    if city is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception as err:
        abort(400, 'Not a JSON')

    if 'name' in data.keys() and 'user_id' in data.keys():
        user_id = data.get('user_id')
        user = storage.get(storage.classes['User'], user_id)
        if user is None:
            abort(404)

        new_place = Place(name=data.get('name'), user_id=data.get('user_id'), city_id=city_id)
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(new_place, key, value)

         new_place.save()
         return new_place.to_dict(), 201

    elif 'user_id' not in data.keys():
        abort(400, 'Missing user_id')

    else:
        abort(400, 'Missing name')



@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    try:
        data = request.get_json()
    except Exception as err:
        abort(400, 'Not a JSON')

    place = storage.get(storage.classes['Place'], place_id)
    if place is None:
        abort(404)

    for key, value in data.items():
        if key not in ['user_id', 'city_id', 'id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()

    return place.to_dict(), 200
