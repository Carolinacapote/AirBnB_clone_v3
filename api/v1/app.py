#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """ This method calls the close() function """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Method to handle errors """

    return {"error": "Not Found"}, 404


@app.errorhandler(400)
def handle_error(error):
    """ Method to handle errors """

    return {"error": error.description}, 400


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST')
    if host is None:
        host = '0.0.0.0'
    port = getenv('HBNB_API_PORT')
    if port is None:
        port = 5000
    app.run(host=host, port=port, threaded=True, debug=True)
