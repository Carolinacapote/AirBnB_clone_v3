#!/usr/bin/python3
"""
declare the views for reviews
"""
from api.v1.views import app_views
from models import storage
from models.review import Review
from flask import abort
from flask import jsonify
from flask import request


@app_views.route('places/<id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews_by_place(id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get(storage.classes['Place'], id)
    if place is None:
        abort(404)
    print(place.reviews)
    return jsonify([rev.to_dict() for rev in place.reviews]), 200


@app_views.route('/reviews/<id>', methods=['GET'], strict_slashes=False)
def get_review(id):
    """ Retrieves the Review objects with the given id  """

    review = storage.get(storage.classes['Review'], id)
    if review is None:
        abort(404)

    return review.to_dict(), 200


@app_views.route('/reviews/<id>', methods=['DELETE'], strict_slashes=False)
def delete_review(id):
    """ Deletes a Review object """
    review = storage.get(storage.classes['Review'], id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()
    return {}, 200


@app_views.route('/places/<id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(id):
    """ Creates a Review object """
    try:
        data = request.get_json()
    except Exception as err:
        abort(400, 'Not a JSON')

    place = storage.get(storage.classes['Place'], id)
    if place is None:
        abort(404)

    if 'user_id' not in data.keys():
        abort(400, 'Missing user_id')

    user = storage.get(storage.classes['User'], data['user_id'])
    if user is None:
        abort(404)

    if 'text' not in data.keys():
        abort(400, 'Missing text')

    new_review = Review(place_id=id)
    for key, attr in data.items():
        if key not in ['id']:
            setattr(new_review, key, attr)

    new_review.save()
    return new_review.to_dict(), 201


@app_views.route('/reviews/<id>', methods=['PUT'], strict_slashes=False)
def update_review(id):
    """ Updates a Review object """
    review = storage.get(storage.classes['Review'], id)
    if review is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception as err:
        abort(400, 'Not a JSON')

    ignored_attrs = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    for key, attr in data.items():
        if key not in ignored_attrs:
            setattr(review, key, attr)
    review.save()

    return review.to_dict(), 200
