from common.settings.common_settings import *  # noqa
import os


BASE_PATH = os.path.dirname(os.path.dirname(__file__))
DEBUG = False

# Protofiles Settings
PROTOFILES_DIRECTORY = os.path.join(BASE_PATH, 'protobuf')
PROTOFILES_NEEDED += []

# ElasticSearch Configuration
USE_ES = False
