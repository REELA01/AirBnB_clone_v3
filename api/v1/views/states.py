#!/usr/bin/python3
"""the states """
import uuid
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from datetime import datetime


@app_views.route('/states/', methods=['GET'])
def lis_stat():
    """get list of aall state"""
    lis_stat = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(lis_stat)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_stat(state_id):
    """retrieve state object"""
    all_stat = storage.all("State").values()
    stat_ob = [obj.to_dict() for obj in all_stat if obj.id == state_id]
    if stat_ob == []:
        abort(404)
    return jsonify(stat_ob[0])


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_stat(state_id):
    """delete state object"""
    all_stat = storage.all("State").values()
    stat_ob = [obj.to_dict() for obj in all_stat if obj.id == state_id]
    if stat_ob == []:
        abort(404)
    stat_ob.remove(stat_ob[0])
    for obj in all_stat:
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def post_stat():
    """create state"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states = []
    ne_stat = State(name=request.json['name'])
    storage.new(ne_stat)
    storage.save()
    states.append(ne_stat.to_dict())
    return jsonify(states[0]), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_stat(state_id):
    """update state object"""
    all_stat = storage.all("State").values()
    stat_ob = [obj.to_dict() for obj in all_stat if obj.id == state_id]
    if stat_ob == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    stat_ob[0]['name'] = request.json['name']
    for obj in all_stat:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(stat_ob[0]), 200
