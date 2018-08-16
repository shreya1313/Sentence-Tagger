"""
this __init__ file is moved in the descriptors on
server startup. it contains the code for importing
all the descriptors that are created using the proto
files. this file will take in all the descriptor
objects specified in the internal as well as the
external proto configurations and import it with:
    from descriptors import <Descriptor_Name>

proto configurations not mentioned cannot be imported.
"""

from flask import current_app as app
from google.protobuf.internal.python_message import \
    GeneratedProtocolMessageType
import importlib
from functools import reduce
import os
import sys


# adds this directory in the path
current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)


def convert_proto_to_descriptor_file(filename):
    return '{}_pb2'.format(filename.split('.')[0])


def get_message_objects(module_name):
    """
    returns all the message objects
    """

    messages = []

    module = importlib.import_module('descriptors.{}'.format(module_name))

    all_objects = [item for item in dir(module)
                   if not item.startswith('__')]

    for obj in all_objects:
        if type(getattr(module, obj)) == GeneratedProtocolMessageType:
            messages.append((obj, getattr(module, obj)))

    return messages


all_proto_files = [
    f for dp, dn, filenames in os.walk(app.config['PROTOFILES_DIRECTORY'])
    for f in filenames if os.path.splitext(f)[1] == '.proto'
]

descriptor_files = list(map(convert_proto_to_descriptor_file,
                            all_proto_files))

all_messages = list(map(get_message_objects, descriptor_files))

messages = reduce(lambda a, x: a + x, all_messages, [])

for message in messages:
    globals().update({message[0]: message[1]})
