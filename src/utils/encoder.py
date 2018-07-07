from flask.json import JSONEncoder
from enum import Enum


class JSONEnumEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value

        return JSONEncoder.default(self, obj)
