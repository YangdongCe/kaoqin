# -*- coding: utf-8 -*-
# @Time    : 2018/6/1 20:42
# @File    : app.py
# @Software: PyCharm
from flask import Flask, request
from flask_cors import CORS
from server import get_feature
from gevent import pywsgi
import json

app = Flask(__name__)
CORS(app)
computeFeature = get_feature()
# default route
@app.route('/')
def index():
    return "Index API"

# HTTP Errors handlers
@app.errorhandler(404)
def url_error(e):
    return """
    Wrong URL!
    <pre>{}</pre>""".format(e), 404

@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

# API route
@app.route('/api',methods=['POST'])
def api():
    """
    :return: 128纬特征向量 list
    """
    if request.method=='POST':
        input_data = request.form['img']
        faceFeature = computeFeature(input_data)
        response = json.dumps({'faceFeature':faceFeature})
        return response

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('127.0.0.1', 1080), app)
    server.serve_forever()
