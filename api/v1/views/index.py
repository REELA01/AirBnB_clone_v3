#!/usr/bin/python3
"""index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review

classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}


@app_views.route('/status', methods=['GET'])
def status():
    """git to status page"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def stat():
    """get number of each objects by type"""
    count_dic = {}
    for cls in classes:
        count_dic[cls] = storage.count(classes[cls])
    return jsonify(count_dic)
