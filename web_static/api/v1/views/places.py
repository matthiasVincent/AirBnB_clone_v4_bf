#!/usr/bin/python3
"""
 New view for Places objects that handles all default RestFul API actions.
"""
from models.place import Place
from models.city import City
from models import storage
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views


@app_views.route('/places', strict_slashes=False, methods=['GET'])
def all_places():
    """ Retrieves the list of all Place objects. """
    list_of_places = []
    for value in storage.all('Place').values():
        list_of_places.append(value.to_dict())
    return jsonify(list_of_places)


@app_views.route('/cities', strict_slashes=False, methods=['GET'])
def all_cities():
    """ Retrieves the list of all City objects. """
    list_of_cities = []
    for value in storage.all('City').values():
        list_of_cities.append(value.to_dict())
    return jsonify(list_of_cities)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def all_places_of_a_city(city_id):
    """ Retrieves the list of all Place objects of a City. """
    list_of_places = []
    full_city = storage.get('City', city_id)
    if not full_city:
        abort(404)
    for city in storage.all('Place').values():
        if city.to_dict()["city_id"] == city_id:
            list_of_places.append(city.to_dict())
    return jsonify(list_of_places)


@app_views.route('/places/<place_id>', methods=['GET'])
def specific_place(place_id):
    """ Retrieves a Place object. """
    full_place = storage.get("Place", place_id)
    if full_place is None:
        abort(404)
    return jsonify(full_place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ Deletes a Place object. """
    full_place = storage.get('Place', place_id)
    if full_place:
        storage.delete(full_place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """ Creates a Place. """
    dic = request.get_json()
    full_city = storage.get('City', city_id)
    full_user = storage.get('User', dic["user_id"])
    if not full_city:
        abort(404)
    if not full_user:
        abort(404)
    if not dic:
        abort(400, {'Not a JSON'})
    if 'name' not in dic:
        abort(400, {'Missing name'})
    if 'user_id' not in dic:
        abort(400, {'Missing user_id'})
    new_place = Place(**dic)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def updates_place(place_id):
    """ Updates a Place object. """
    dic = request.get_json()
    selected_place = storage.get('Place', place_id)
    if not selected_place:
        abort(404)
    if not dic:
        abort(400, {'Not a JSON'})
    for key, value in dic.items():
        if key not in ['id', 'user_id', 'city_id', 'updated_at', 'created_at']:
            setattr(selected_place, key, value)
    storage.save()
    return jsonify(selected_place.to_dict()), 200
