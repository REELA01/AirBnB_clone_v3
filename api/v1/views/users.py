#!/usr/bin/python3
""" the user"""
import uuid
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from datetime import datetime


@app_views.route('/users/', methods=['GET'])
@app_views.route('/users', methods=['GET'])
def lis_user():
    """git list of all user objects"""
    lis_us = [obj.to_dict() for obj in storage.all("User").values()]
    return jsonify(list_use)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """git  a user object"""
    all_us = storage.all("User").values()
    us_ob = [obj.to_dict() for obj in all_us if obj.id == user_id]
    if us_ob == []:
        abort(404)
    return jsonify(us_ob[0])


@app_views.route('/users/<user_id>', methods=['DELETE'])
def del_user(user_id):
    """delete a user object"""
    all_us = storage.all("User").values()
    us_ob = [obj.to_dict() for obj in all_us if obj.id == user_id]
    if us_ob == []:
        abort(404)
    us_ob.remove(us_ob[0])
    for obj in all_us:
        if obj.id == user_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def post_user():
    """creates a user"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing name')
    if 'password' not in request.get_json():
        abort(400, 'Missing name')
    users = []
    ne_us = User(email=request.json['email'],
                    password=request.json['password'])
    storage.new(ne_us)
    storage.save()
    users.append(ne_us.to_dict())
    return jsonify(users[0]), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """update a user object"""
    all_us = storage.all("User").values()
    us_ob = [obj.to_dict() for obj in all_us if obj.id == user_id]
    if us_ob == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    try:
        us_ob[0]['first_name'] = request.json['first_name']
    except:
        pass
    try:
        us_ob[0]['last_name'] = request.json['last_name']
    except:
        pass
    for obj in all_us:
        if obj.id == user_id:
            try:
                if request.json['first_name'] is not None:
                    obj.first_name = request.json['first_name']
            except:
                pass
            try:
                if request.json['last_name'] is not None:
                    obj.last_name = request.json['last_name']
            except:
                pass
    storage.save()
    return jsonify(us_ob[0]), 200
