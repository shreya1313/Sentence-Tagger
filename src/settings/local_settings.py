from common.settings.common_settings import *
import os


BASE_PATH = os.path.dirname(os.path.dirname(__file__))

PROTOFILES_DIRECTORY = os.path.join(BASE_PATH, 'protobuf')
DESCRIPTORS_DIRECTORY = os.path.join(BASE_PATH, 'descriptors')

EXTERNAL_PROTOBUF_CONFIG = []
