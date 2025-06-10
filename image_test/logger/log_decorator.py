import tracemalloc
from functools import wraps
from time import time
from typing import Callable

from image_test.logger.log_function import log_complete, log_error, log_start


def time_memory_logger(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        class_name = args[0].__class__.__name__
        log_start(class_name)

        tracemalloc.start()
        start_time = time()

        try:
            result = await func(*args, **kwargs)
            end_time = time()
            _, peak = tracemalloc.get_traced_memory()
            log_complete(class_name, start_time, end_time, peak)
            return result
        except Exception as e:
            log_error(class_name, start_time, e)

    return wrapper
