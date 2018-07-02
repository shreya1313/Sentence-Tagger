from threading import local
from logging import getLogger


_locals = local()
logger = getLogger(__name__)


def get_trace_id():
    """Get the current identifier of the request/task etc."""
    return getattr(_locals, 'trace_id', u'INTERNAL')


def set_trace_id(trace_id):
    """Set the current identifier of the request/task etc."""
    _locals.trace_id = trace_id
    logger.debug('TraceId %s set for the request', trace_id)


def delete_trace_id():
    """Delete the current identifier of the request/task etc."""

    if not hasattr(_locals, 'trace_id'):
        return

    logger.debug('Removing TraceId %s from thread local storage',
                 _locals.trace_id)
    del _locals.trace_id
