#!/usr/bin/python3
""" the amenities """
import uuid
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from datetime import datetime


@app_views.route('/amenities/', methods=['GET'])
def lis_amenity():
    """get a list of all amenity objects"""
    lis_amenity = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(lis_amenity)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """get an amenity object"""
    all_amen = storage.all("Amenity").values()
    amen_ob = [obj.to_dict() for obj in all_amen
                   if obj.id == amenity_id]
    if amen_ob == []:
        abort(404)
    return jsonify(amen_ob[0])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def del_amenity(amenity_id):
    """delete an amenity object"""
    all_amen = storage.all("Amenity").values()
    amen_ob = [obj.to_dict() for obj in all_amen
                   if obj.id == amenity_id]
    if amen_ob == []:
        abort(404)
    amen_ob.remove(amen_ob[0])
    for obj in all_amen:
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def post_amenity():
    """create an amenity"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenities = []
    ne_amen = Amenity(name=request.json['name'])
    storage.new(ne_amen)
    storage.save()
    amenities.append(ne_amen.to_dict())
    return jsonify(amenities[0]), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """update an amenity object"""
    all_amen = storage.all("Amenity").values()
    amen_ob = [obj.to_dict() for obj in all_amen
                   if obj.id == amenity_id]
    if amen_ob == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    amen_ob[0]['name'] = request.json['name']
    for obj in all_amen:
        if obj.id == amenity_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(amen_ob[0]), 200
