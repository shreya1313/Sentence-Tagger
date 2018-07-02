from utils.trace_utils import get_trace_id, set_trace_id, \
    delete_trace_id


def set_trace_id_arg(body=None, **kwargs):
    trace_id = get_trace_id()
    task_kwargs = body[1]
    task_kwargs.update({"SPOTMENTOR_TRACE_ID": trace_id})


def set_trace_id_local(args=None, kwargs=None, **extra_kwargs):
    trace_id = kwargs.pop('SPOTMENTOR_TRACE_ID')
    set_trace_id(trace_id)


def delete_trace_id_local(args=None, kwargs=None, **extra_kwargs):
    delete_trace_id()
