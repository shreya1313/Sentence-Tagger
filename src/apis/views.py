import logging
from tasks import test_task
from flask import current_app as app
from flask import send_from_directory
from utils.pbj import api, protobuf
from descriptors import Scaffolding


logger = logging.getLogger(__name__)
APPLICATION_NAME = app.config['APPLICATION_NAME']


def index():
    """
    index view for testing loggers and task
    """
    test_task.delay()
    logger.info("Checking the {} logger".format(APPLICATION_NAME))
    return "Welcome to the {} application".format(APPLICATION_NAME)


def error():
    """
    api view for testing the error
    """

    a = [0, 1]

    return a[10]


def serve_proto_files(name):
    """
    serves the proto files easily accessible to other microservices
    or gateways
    """

    proto_dir = app.config['PROTOFILES_DIRECTORY']

    return send_from_directory(proto_dir, name)


@api(protobuf(sends=Scaffolding))
def proto():
    """
    api view for testing protobuf serialization/deserialization
    """

    data = {'name': 'Flask Scaffolding', 'scaffolding_type': 1}

    return data
