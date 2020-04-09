from flask import render_template, request, Response

from app import app
from .config import topic_name, bootstrap as kafka_bootstrap
import dto


@app.route('/')
def index():
    return render_template('index.j2', kafka_bootstrap=kafka_bootstrap)


@app.route('/generate', methods=['GET'])
def generate():
    args = request.args
    count = int(args.get('c', 1))
    dto.generate_data(count, topic_name=topic_name)
    return Response('data sent', status=202)


@app.route('/<username>')
def hello(username):
    return render_template('index.j2', username=username,
                           kafka_bootstrap=kafka_bootstrap)
