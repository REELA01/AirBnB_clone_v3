#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON"""

from flask import jsonify
import models
from models import storage
from models.base_model import BaseModel
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """return json"""
    return jsonify(status='OK')


@app_views.route('/stats', strict_slashes=False)
def status02():
    """return the responese"""
    cls_name = {'states': State, 'users': User,
            'amenities': Amenity, 'cities': City,
            'places': Place, 'reviews': Review}
    for ke in cls_name:
        cls_name[ke] = storage.count(cls_name[ke])
    return jsonify(cls_name)
