#!/usr/bin/python3
"""
route for amenities
"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def amenities():
    """method to get amenities"""
    if request.method == 'GET':
        amenities = storage.all("Amenity").values()
        return jsonify([amen.to_dict() for amen in amenities])
    if request.method == 'POST':
        data = request.get_json()

        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')

        amenity = Amenity(**data)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def amenity(amenity_id):
    """gets a specific amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404, 'Not a JSON')
    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return {}, 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        ignore = ('id', 'created_at', 'updated_at')
        for k, v in data.items():
            if k not in ignore:
                setattr(amenity, k, v)
        storage.save()
        return jsonify(amenity.to_dict()), 200
