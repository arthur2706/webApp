from flask import Flask, request, jsonify
from redis import Redis, RedisError
from jsonifyexcept import jsonifyexcept
import os
import socket
import hashlib

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)
sha256 = hashlib.sha256()

app = Flask(__name__)

@app.route("/")
@jsonifyexcept
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
@jsonifyexcept
def messages():
    msg = request.get_json()["message"].encode('utf-8')
    sha256.update(msg)
    hash = sha256.hexdigest()
    redis.set(str(hash), msg)
    return jsonify(digest=str(hash))


@app.route('/messages/<string:hash>', methods=['GET'])
@jsonifyexcept
def search(hash):
    msg = redis.get(hash)
    if msg:
        return jsonify(message=msg)
    else:
        raise Exception("Message not found")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
