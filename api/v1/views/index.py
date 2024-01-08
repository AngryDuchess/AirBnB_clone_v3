from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """returns a json"""
    return jsonify({'status': 'OK'})
