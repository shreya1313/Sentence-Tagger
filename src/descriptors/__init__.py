# """
# this __init__ file is moved in the descriptors on
# server startup. it contains the code for importing
# all the descriptors that are created using the proto
# files. this file will take in all the descriptor
# objects specified in the internal as well as the
# external proto configurations and import it with:
#     from descriptors import <Descriptor_Name>

# proto configurations not mentioned cannot be imported.
# """

# from flask import current_app as app
# from google.protobuf.internal.python_message import \
#     GeneratedProtocolMessageType
# import itertools
# import importlib
# from functools import reduce


# externals = app.config['EXTERNAL_PROTOBUF_CONFIG']
# internals = app.config['INTERNAL_PROTOBUF_CONFIG']

# external_protos = []
# internal_protos = []


# def get_all_file_names(config_list):
#     """
#     returns all the file names
#     """
#     files = reduce(lambda a, x: a + x, config_list, [])

#     all_urls = map(lambda datum: datum.get('file_url'),
#                    files)

#     return [url.split('/')[-1] for url in all_urls]


# def get_message_objects(module_name):
#     """
#     returns all the message objects
#     """

#     messages = []

#     module = importlib.import_module('descriptors.{}'.format(module_name))

#     all_objects = [item for item in dir(module)
#                    if not item.startswith('__')]

#     for obj in all_objects:
#         if type(getattr(module, obj)) == GeneratedProtocolMessageType:
#             messages.append((obj, getattr(module, obj)))

#     return messages


# if externals:
#     all_names = get_all_file_names(list(externals.values()))

#     all_messages = map(get_message_objects, all_names)

#     external_protos = reduce(lambda a, x: a + x, all_messages, [])


# if internals:
#     all_names = get_all_file_names(list(internals.values()))

#     all_messages = map(get_message_objects, all_names)

#     internal_protos = reduce(lambda a, x: a + x, all_messages, [])


# for proto in itertools.chain(external_protos, internal_protos):
#     print('Updating Proto: {}'.format(proto))
#     globals().update({proto[0]: proto[1]})
