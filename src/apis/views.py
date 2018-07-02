import logging
from tasks import test_task
from flask import current_app as app


logger = logging.getLogger("default")
APPLICATION_NAME = app.config['APPLICATION_NAME']


def index():
    test_task.delay()
    logger.info("Checking the {} logger".format(APPLICATION_NAME))
    return "Welcome to the {} application".format(APPLICATION_NAME)
