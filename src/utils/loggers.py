import logging
import os
import errno
from utils.trace_utils import get_trace_id
from flask import current_app as app


def mkdir_p(filename):
    path = os.path.dirname(filename)
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class MakeFileHandler(logging.handlers.TimedRotatingFileHandler):
    """
    Make file handler
    """
    def __init__(self, filename, when='d', interval=1,
                 backupCount=7, encoding=None, delay=True,
                 utc=False):
        super(MakeFileHandler, self).__init__('/dev/null', when,
                                              interval, backupCount,
                                              encoding, delay, utc)

        if 'SPOTMENTOR_SERVICE_NAME' in app.config:
            filename = "{}_{}".format(
                app.config['SPOTMENTOR_SERVICE_NAME'], filename
            )

        self.baseFilename = os.path.join(app.config['LOG_ROOT'],
                                         filename)
        mkdir_p(self.baseFilename)

    def _open(self):
        return super(MakeFileHandler, self)._open()


class TraceIdFilter(logging.Filter):
    """Add Trace ID to the context of a log record."""

    def filter(self, record):
        record.traceid = get_trace_id()
        return True
