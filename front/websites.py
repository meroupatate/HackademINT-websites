import json, requests
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
API_URL = 'https://websites-api.priv.hackademint.org/stats'
s = requests.session()


@app.route("/")
def index():
    data = s.get(API_URL).content
    j = json.loads(data.decode())
    data = [ j[i] for i in j ]
    return render_template('index.html', data=data)


@app.route('/stats')
def stats():
    data = s.get(API_URL).content
    j = json.loads(data.decode())
    data = [ j[i] for i in j ]
    return render_template('stats.html', data=data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7654)
