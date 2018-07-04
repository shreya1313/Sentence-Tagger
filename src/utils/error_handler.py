from flask import jsonify
import logging
import traceback


logger = logging.getLogger(__name__)


def handle_invalid_usage(error):
    response = jsonify({'errorMessage': repr(error)})

    logger.error(
        'following error raised: {}'.format(
            "".join(traceback.format_exception(
                type(error), error, error.__traceback__))))

    response.status_code = 400

    return response
