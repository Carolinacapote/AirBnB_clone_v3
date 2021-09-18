#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """ Returns a JSON """
    return {'status': 'OK'}


@app_views.route('/stats')
def stats():
    """ Retrieves the number of each objects by type """
    counters = {}
    for class_name, each_class in storage.classes.items():
        
        name = class_name.casefold()
        if name[-1] == 'y':
            name = name[:-1] + 'ie'
        name = name + 's'

        counters[name] = storage.count(each_class)

    return counters
