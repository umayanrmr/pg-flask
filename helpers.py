import functools

def responseHandler(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return { "data": res }, 200
        except KeyError as e:
            return { "message": "Object not found" }, 404
        
    return decorator