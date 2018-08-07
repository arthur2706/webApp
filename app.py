from flask import Flask, request, jsonify, abort
from redis import Redis, RedisError
from validate import ValidateInputs
import os
import socket
from hashlib import sha256
import functools

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)


def except404(function):
    """
    A decorator that aborts with 404 not found.
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            abort(404, jsonify(err_msg=e.message))

    return wrapper


def redisping(function):
    """
    A decorator that pings redis to check connection
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            redis.ping()
            return function(*args, **kwargs)
        except RedisError:
            raise Exception("cannot connect to Redis")

    return wrapper


@app.route("/")
@redisping
@except404
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)


@app.route('/messages', methods=['POST'])
@redisping
@except404
def hashmsg():
    inputs = ValidateInputs(request)
    if not inputs.validate():
        raise Exception("validation errros: {}".format(inputs.errors))

    msg = request.get_json()["message"].encode('utf-8')
    hasher = sha256(msg)
    hash = hasher.hexdigest()
    redis.set(str(hash), msg)
    return jsonify(digest=str(hash))


@app.route('/messages/<string:hash>', methods=['GET'])
@redisping
@except404
def search(hash):
    msg = redis.get(hash)
    if msg:
        return jsonify(message=msg)
    else:
        raise Exception("Message not found")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
