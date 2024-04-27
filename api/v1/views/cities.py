#!/usr/bin/python3
""" the cities """
import uuid
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from datetime import datetime


@app_views.route('/states/<state_id>/cities', methods=['GET'])
@app_views.route('/states/<state_id>/cities/', methods=['GET'])
def lis_cities(state_id):
    """get list of City objects"""
    all_stat = storage.all("State").values()
    stat_ob = [obj.to_dict() for obj in all_stat if obj.id == state_id]
    if stat_ob == []:
        abort(404)
    lis_cities = [obj.to_dict() for obj in storage.all("City").values()
                   if state_id == obj.state_id]
    return jsonify(lis_cities)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def post_cities(state_id):
    """post a City"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    all_stat = storage.all("State").values()
    stat_ob = [obj.to_dict() for obj in all_stat if obj.id == state_id]
    if stat_ob == []:
        abort(404)
    cities = []
    ne_cities = City(name=request.json['name'], state_id=state_id)
    storage.new(ne_cities)
    storage.save()
    cities.append(ne_cities.to_dict())
    return jsonify(cities[0]), 201


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_cities(city_id):
    """git acity object"""
    all_cit = storage.all("City").values()
    cit_ob = [obj.to_dict() for obj in all_cit if obj.id == city_id]
    if cit_ob == []:
        abort(404)
    return jsonify(cit_ob[0])


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def del_cities(city_id):
    """delete city object"""
    all_cit = storage.all("City").values()
    cit_ob = [obj.to_dict() for obj in all_cit if obj.id == city_id]
    if cit_ob == []:
        abort(404)
    cit_ob.remove(cit_ob[0])
    for obj in all_cit:
        if obj.id == city_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_cities(city_id):
    """updates city object"""
    all_cit = storage.all("City").values()
    cit_ob = [obj.to_dict() for obj in all_cit if obj.id == city_id]
    if cit_ob == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    cit_ob[0]['name'] = request.json['name']
    for obj in all_cit:
        if obj.id == city_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(cit_ob[0]), 200
