import functools
from flask import jsonify

def jsonifyexcept(function):
    """
    A decorator that returns a json error.
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            return jsonify(err_msg=e.message)

    return wrapper