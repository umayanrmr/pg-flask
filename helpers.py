import functools
from flask_smorest import abort

def responseHandler(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return { "data": res }, 200
        except KeyError as e:
            abort(404, message="Item not found")
        
    return decorator