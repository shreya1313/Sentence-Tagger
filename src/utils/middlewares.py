from uuid import uuid4
from utils.trace_utils import set_trace_id, delete_trace_id, get_trace_id
from flask import request


def set_trace_id_middleware():
    """
    sets the trace id
    """

    if 'SPOTMENTOR_TRACE_ID' in request.headers:
        set_trace_id(request.headers.get('SPOTMENTOR_TRACE_ID'))

        return

    trace_id = str(uuid4())
    set_trace_id(trace_id)


def delete_trace_id_middleware(response):
    """
    deletes the trace id
    """

    try:
        response.headers['SPOTMENTOR_TRACE_ID'] = get_trace_id()
    except AttributeError:
        # trace_id has not been set
        return response

    delete_trace_id()

    return response
