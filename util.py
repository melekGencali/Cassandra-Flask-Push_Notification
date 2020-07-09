import json

__author__ = 'melek'


def to_json(data):
    def handler(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise print(TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))

    return json.dumps(data, default=handler)