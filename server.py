
import jinja2
import jgrabber
import os

from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask.json import jsonify
from werkzeug import SharedDataMiddleware

APP_ROOT = os.path.dirname(__file__)
url = lambda u: os.path.join(APP_ROOT, u)

app = Flask(__name__)
app.config.from_pyfile('settings.py')

app.jinja_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(url('static'))
])

app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/': os.path.join(os.path.dirname(__file__), 'static'),
})


@app.route('/')
def home():
    return send_from_directory('static', 'index.html')


@app.route('/api')
def api_home():
    return 'Stop kidding and request an actual API endpoint.'


@app.route('/api/jobs')
def get_jobs():
    stuff = jgrabber.get_jobs(app.config['JENKINS_SERVER'])
    return jsonify({'jobs': stuff})


@app.route('/api/job/<job_name>/tests')
def get_jenkins_data(job_name):
    stuff = jgrabber.get_job_tests(app.config['JENKINS_SERVER'], job_name)
    return jsonify({'tests': stuff})


@app.route('/api/job/<job_name>/test/<test>')
def get_test_data(job_name, test):
    stuff = jgrabber.get_test_data(app.config['JENKINS_SERVER'], job_name,
                                   test)
    return jsonify(stuff)


if __name__ == '__main__':
    app.run(debug=True)
