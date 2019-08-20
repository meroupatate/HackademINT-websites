#!/usr/bin/python3

import requests
import json
from flask import Flask, render_template
from flask_caching import Cache
from src.functions import get_websites_jobs 

cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
cache.init_app(app)


@app.route("/")
@cache.cached(timeout=60)
def index():
    websites = get_websites_jobs()
    return render_template('index.html', websites=websites)


@app.route('/stats')
@cache.cached(timeout=60)
def stats():
    websites = get_websites_jobs()
    return render_template('stats.html', websites=websites)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
