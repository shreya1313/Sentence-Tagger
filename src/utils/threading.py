import time
import multiprocessing
import traceback
from functools import partial


def time_profiler(func, task="unspecified", args=[], **kwargs):
    """
    profiles time for small functions
    which do not use multiprocessing
    """

    current_time = time.time()
    print("`{0}` task started at {1}".format(
        task, time.asctime(time.localtime(current_time))))

    output = func(*args, **kwargs)

    print("`{0}` task completed in {1} seconds".format(
        task, time.time() - current_time))

    return output


def map_multiprocessing(function, sequence,
                        processes=multiprocessing.cpu_count()):
    """
    sequence based multiprocessing
    """
    pool = multiprocessing.Pool(processes)

    try:
        results = time_profiler(
            func=pool.map,
            task='(MULTI:{}) {}'.format(
                processes,
                function.__name__ if not type(function) is partial
                else 'partial',
            ),
            args=[function, sequence],
        )

        pool.close()

        return results
    except Exception as ex:
        traceback.print_exc()
        pool.terminate()
        raise ex
