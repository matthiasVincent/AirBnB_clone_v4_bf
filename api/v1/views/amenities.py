#!/usr/bin/python3
"""
 New view for Amenities objects that handles all default RestFul API actions.
"""
from models.amenity import Amenity
from models import storage
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def all_amenities():
    """ Retrieves the list of all Amenity objects. """
    list_of_amenities = []
    for value in storage.all('Amenity').values():
        list_of_amenities.append(value.to_dict())
    return jsonify(list_of_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def specific_amenity(amenity_id):
    """ Retrieves a Amenity object. """
    full_amenity = storage.get("Amenity", amenity_id)
    if full_amenity is None:
        abort(404)
    return jsonify(full_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Deletes a Amenity object. """
    full_amenity = storage.get('Amenity', amenity_id)
    if full_amenity:
        storage.delete(full_amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """ Creates a Amenity. """
    dic = request.get_json()
    if not dic:
        abort(400, {'Not a JSON'})
    if 'name' not in dic:
        abort(400, {'Missing name'})
    new_amenity = Amenity(**dic)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('amenities/<amenity_id>', methods=['PUT'])
def updates_amenity(amenity_id):
    """ Updates a State object. """
    dic = request.get_json()
    selected_amenity = storage.get('Amenity', amenity_id)
    if not selected_amenity:
        abort(404)
    if not dic:
        abort(400, {'Not a JSON'})
    for key, value in dic.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(selected_amenity, key, value)
    storage.save()
    return jsonify(selected_amenity.to_dict()), 200
