from functools import wraps

from flask import g, abort


def user_required(f):

    @wraps(f)
    def decorator(*args, **kwargs):
        if g.user is None:
            abort(404)
        else:
            return f(*args, **kwargs)
    return decorator

