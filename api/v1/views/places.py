#!/usr/bin/python3
"""
route for places
"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from models.user import User
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def city_places(city_id):
    """gets the cities to a place"""
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        return jsonify([place.to_dict() for place in city.places])
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        user = storage.get(User, data.get('user_id'))
        if not user:
            abort(404)
        data['city_id'] = city_id
        place = Place(**data)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def places(place_id):
    """gets a specific place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return {}, 200
    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        ignore = ('id', 'created_at', 'updated_at', 'user_id', 'city_id')
        for k, v in data.items():
            if k not in ignore:
                setattr(place, k, v)
        storage.save()
        return jsonify(place.to_dict()), 200
