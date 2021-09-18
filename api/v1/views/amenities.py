#!/usr/bin/python3
"""
declare the viws for amenities 
"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort
from flask import jsonify
from flask import request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<id>', methods=['GET'], strict_slashes=False)
def get_amenities(id=None):
    """ Retrieves the list of all Amenity objects or a amenity object by Id """
    if id is None:
        amenities = storage.all(storage.classes['Amenity'])
        return jsonify([obj.to_dict() for obj in amenities.values()])

    else:
        amenity = storage.get(storage.classes['Amenity'], id)
        if amenity is None:
            abort(404)
        return amenity.to_dict(), 200


@app_views.route('/amenities/<id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(id):
    """ Deletes a Amenity object """
    amenity = storage.get(storage.classes['Amenity'], id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()
    return {}, 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates a Amenity object """
    try:
        data = request.get_json()
    except Exception as err:
        abort(400, 'Not a JSON')

    if 'name' in data.keys():
        new_amenity = Amenity(name=data.get('name'))
        new_amenity.save()
        return new_amenity.to_dict(), 201
    else:
        abort(400, 'Missing name')


@app_views.route('/amenities/<id>', methods=['PUT'], strict_slashes=False)
def update_amenity(id):
    """ Updates a Amenity object """
    try:
        data = request.get_json()
    except Exception as err:
        abort(400, 'Not a JSON')

    amenity = storage.get(storage.classes['Amenity'], id)
    if amenity is None:
        abort(404)

    

    for key, attr in data.items():
        if key not in ['id', 'created_at', 'updated_at']: 
            setattr(amenity, key, attr)
    amenity.save()


    return amenity.to_dict(), 200
