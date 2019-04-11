#!/usr/bin/python3

import requests, os

from flask import Flask
from flask import render_template
from flask import render_template_string, abort
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
cache.init_app(app)

POSTGRES = {
    'user': 'websites',
    'pw': open('./pass', 'r').read()[:-1],
    'db': 'websites',
    'host': '10.10.10.6',
    'port': '5432'
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Websites(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), unique=True, nullable=False)
    ip = db.Column(db.String(500), unique=False, nullable=True)
    port = db.Column(db.String(500), unique=False, nullable=True)
    protocol = db.Column(db.String(500), unique=False, nullable=True)

@app.route("/")
@cache.cached(timeout=60)
def index():
    data = []
    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3004, debug=True)
