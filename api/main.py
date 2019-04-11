#!/usr/bin/python3

import requests
from flask import Flask, jsonify
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
    author = 'lishizalice'
    follow_me = 'https://github.com/lishizalice'
    d = {'author': author, 'follow_me': follow_me}
    return jsonify(d)


@app.route('/stats')
@cache.cached(timeout=60)
def stats():
    websites = Websites.query.all()
    d = {}
    for key, website in enumerate(websites):
        if not website.protocol:
            continue
        if website.port:
            pattern = '{}://{}:{}'
        else:
            pattern = '{}://{}'
        try:
            f = pattern.format(website.protocol, website.ip, website.port)
            status_code = requests.get(f, verify=False, stream=True, timeout=0.1).status_code
        except Exception as exception:
            print(exception)
            status_code = 404
        d[str(key)] = {'id': website.id, 'url': website.url, 'ip': website.ip,
                       'port': website.port, 'protocol': website.protocol,
                       'status_code': status_code}
    return jsonify(d)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7653, debug=True)
