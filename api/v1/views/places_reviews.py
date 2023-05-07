#!/usr/bin/python3
"""
 New view for Reviews objects that handles all default RestFul API actions.
"""
from models.place import Place
from models.review import Review
from models import storage
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views


@app_views.route('/reviews', strict_slashes=False, methods=['GET'])
def all_reviews():
    """ Retrieves the list of all Review objects. """
    list_of_reviews = []
    for value in storage.all('Review').values():
        list_of_review.append(value.to_dict())
    return jsonify(list_of_reviews)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def all_reviews_of_a_place(place_id):
    """ Retrieves the list of all Review objects of a Place. """
    list_of_reviews = []
    full_place = storage.get('Place', place_id)
    if not full_place:
        abort(404)
    for place in storage.all('Review').values():
        list_of_places.append(city.to_dict())
    return jsonify(list_of_places)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def specific_review(review_id):
    """ Retrieves a Review object. """
    full_review = storage.get("Review", review_id)
    if full_review is None:
        abort(404)
    return jsonify(full_review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ Deletes a Review object. """
    full_review = storage.get('Review', review_id)
    if full_review:
        storage.delete(full_review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def create_Review(place_id):
    """ Creates a Review. """
    dic = request.get_json()
    full_place = storage.get('Place', place_id)
    full_user = storage.get('User', dic["user_id"])
    if not full_place:
        abort(404)
    if not full_user:
        abort(404)
    if not dic:
        abort(400, {'Not a JSON'})
    if 'text' not in dic:
        abort(400, {'Missing text'})
    if 'user_id' not in dic:
        abort(400, {'Missing user_id'})
    dic["place_id"] = place_id
    new_review = Review(**dic)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def updates_review(review_id):
    """ Updates a Review object. """
    dic = request.get_json()
    selected_review = storage.get('Review', review_id)
    if not selected_review:
        abort(404)
    if not dic:
        abort(400, {'Not a JSON'})
    for key, value in dic.items():
        if key not in ['id', 'user_id', 'place_id',
                       'updated_at', 'created_at']:
            setattr(selected_review, key, value)
    storage.save()
    return jsonify(selected_review.to_dict()), 200
