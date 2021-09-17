#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """ Returns a JSON """
    return {'status': 'OK'}
