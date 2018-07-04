import logging
from tasks import test_task
from flask import current_app as app


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
