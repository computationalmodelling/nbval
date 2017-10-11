import pickle
import base64

def tmp_load(x):
    return pickle.loads(base64.b64decode(x.encode('utf-8')))

handlers = {}
handlers['application/json'] = lambda x: tmp_load(x['data'])


def get_handler(x):
    return handlers.get(x, lambda x: x)
