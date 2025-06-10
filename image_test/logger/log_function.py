import textwrap
import traceback
from time import time

from image_test.container.log_container import access_logger
from image_test.logger.log_dto import BaseLogFormat


def log_start(class_name: str):
    access_logger.info(f"Start {class_name}")


def log_complete(class_name: str, start_time: time, end_time: time, peak_memory_usage: int):
    log_format = BaseLogFormat.from_(class_name, start_time, end_time, peak_memory_usage=peak_memory_usage)
    access_logger.info(log_format.__str__())


def log_error(class_name: str, start_time: time, exception: Exception):
    formatted = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
    error_message = textwrap.indent(formatted, "        ")

    log_format = BaseLogFormat.from_(class_name, start_time, time(), message=error_message)
    access_logger.error(log_format.__str__())
