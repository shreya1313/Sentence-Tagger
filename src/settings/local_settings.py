import os
import sys


DEBUG = True
APPLICATION_NAME = os.environ.get('APPLICATION_NAME')
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
ENVIRONMENT = os.environ.get('FLASK_ENV')


LOG_ROOT = os.environ.get("LOG_ROOT")
LOG_FILENAME = "{}.log".format(APPLICATION_NAME)

# Logging configuration

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s %(levelname)s] %(traceid)s '
                      '%(name)s %(message)s'
        },
    },
    'filters': {
        'trace_id_filter': {
            '()': 'utils.loggers.TraceIdFilter'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'utils.loggers.MakeFileHandler',
            'formatter': 'default',
            'encoding': 'utf-8',
            'filename': os.path.join(LOG_ROOT, LOG_FILENAME),
            'filters': ['trace_id_filter'],
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'default',
            'filters': ['trace_id_filter'],
        },
    },
    'root': {
        'handlers': ['console', 'default'],
        'level': 'DEBUG',
    }
}

# Celery Configuration

CELERY_BROKER_URL = 'redis://broker:6379/0'
CELERY_RESULT_BACKEND = 'redis://broker:6379/0'
CELERYD_HIJACK_ROOT_LOGGER = False

# Mongo database settings

MONGO_SETTINGS = {
    'DB_NAME': os.environ.get('DATABASE_NAME'),
    'HOST': os.environ.get('DATABASE_HOST'),
    'PORT': int(os.environ.get('DATABASE_PORT')),
    'USERNAME': os.environ.get('DATABASE_USERNAME'),
    'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
}

# Protofiles Namespace Setup (PNS)
# ================================
# if a particular microservice uses any other protofile from
# a different microservice then all the configuration will come
# here and will be entered as:
# {
#    'content': [{
#        'file_path': '',
#        'message_name': '',
#    }]
# }

PROTOFILES_DIRECTORY = os.path.join(BASE_PATH, 'protobuf')
DESCRIPTORS_DIRECTORY = os.path.join(BASE_PATH, 'descriptors')

EXTERNAL_PROTOBUF_CONFIG = []

# Redis Cache Configuration
CACHE_CONFIGURATION = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': os.environ.get('CACHE_REDIS_HOST'),
    'CACHE_REDIS_PORT': int(os.environ.get('CACHE_REDIS_PORT')),
    'CACHE_REDIS_DB': int(os.environ.get('CACHE_REDIS_DB')),
}
