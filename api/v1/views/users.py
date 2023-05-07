#!/usr/bin/python3
"""
 New view for Users objects that handles all default RestFul API actions.
"""
from models.user import User
from models import storage
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def all_users():
    """ Retrieves the list of all Users objects. """
    list_of_users = []
    for value in storage.all('User').values():
        list_of_users.append(value.to_dict())
    return jsonify(list_of_users)


@app_views.route('/users/<user_id>', methods=['GET'])
def specific_user(user_id):
    """ Retrieves a User object. """
    full_user = storage.get("User", user_id)
    if full_user is None:
        abort(404)
    return jsonify(full_user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Deletes a User object. """
    full_user = storage.get('User', user_id)
    if full_user:
        storage.delete(full_user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """ Creates a User. """
    dic = request.get_json()
    if not dic:
        abort(400, {'Not a JSON'})
    if 'email' not in dic:
        abort(400, {'Missing email'})
    if 'password' not in dic:
        abort(400, {'Missing password'})
    new_user = User(**dic)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('users/<user_id>', methods=['PUT'])
def updates_user(user_id):
    """ Updates a User object. """
    dic = request.get_json()
    selected_user = storage.get('User', user_id)
    if not selected_user:
        abort(404)
    if not dic:
        abort(400, {'Not a JSON'})
    for key, value in dic.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(selected_user, key, value)
    storage.save()
    return jsonify(selected_user.to_dict()), 200
