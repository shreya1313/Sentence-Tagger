from common.settings.common_settings import *  # noqa
from common.utils.event_conf import generate_consumer_exchange_configuration
import os


BASE_PATH = os.path.dirname(os.path.dirname(__file__))
DEBUG = False

# Protofiles Settings
PROTOFILES_DIRECTORY = os.path.join(BASE_PATH, 'protobuf')
DESCRIPTORS_DIRECTORY = os.path.join(BASE_PATH, 'descriptors')
PROTOFILES_NEEDED += []

# ElasticSearch Configuration
USE_ES = False

# Publisher config
PUBLISHER_CONFIG = {}
CONSUMER_CONFIG = {}

EVENT_CONSUMER_QUEUE_NAME_PREFIX = EVENTS_PREFIX
EVENT_CONSUMER_EXCHANGES\
    = generate_consumer_exchange_configuration(
        CONSUMER_CONFIG, DEFAULT_EXCHANGE_TYPE)

# Dependency Injection Flag
USES_DEPENDENCY_INJECTION = False
