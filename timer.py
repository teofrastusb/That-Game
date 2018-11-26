import time

def timed(function):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        ret = function(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{elapsed} seconds for method: {function.__name__}")
        return ret
    return wrapper