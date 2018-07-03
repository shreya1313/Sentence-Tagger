import copy
from mongoengine.base.datastructures import BaseDict, BaseList
from mongoengine import EmbeddedDocument


def to_dict(original_obj):
    obj = copy.deepcopy(original_obj)
    output = dict(obj._data)

    if 'id' in output.keys():
        output['id'] = str(output.get('id'))

    def convert_value(value):
        if isinstance(value, EmbeddedDocument):
            embedded_output = {}
            for key, value in dict(value._data).iteritems():
                embedded_output[key] = convert_value(value)

            return embedded_output

        if (isinstance(value, BaseList) or isinstance(value, list)) and value:
            return [convert_value(instance) for instance in value]

        if (isinstance(value, BaseDict) or isinstance(value, dict)) and value:
            return {
                mapfield_key: convert_value(mapfield_value)
                for mapfield_key, mapfield_value in
                value.iteritems()
            }

        return value

    for key, value in output.iteritems():
        output[key] = convert_value(value)

    return output
