import logging
import logging.handlers
import os
import textwrap
import traceback
from logging import Formatter, Logger
from os.path import join
from typing import Optional

from image_test.config import env_config
from image_test.logger.log_enum import LogLevel


class LogManager(object):
    FORMAT: str = "%(asctime)-11s|%(process)3d|%(threadName)-10s|%(name)-6s|%(levelname)-6s|%(message)s"
    FORMATTER: Formatter = logging.Formatter(FORMAT)

    def __init__(
        self,
        logger_name: str,
        level: LogLevel,
        stream: Optional[bool] = True,
        file: Optional[bool] = True,
        self_rotate: Optional[bool] = False,
    ):
        self.logger = self.create_logger(logger_name, level, stream, file, self_rotate)

    def create_logger(self, logger_name: str, level: LogLevel, stream: bool, file: bool, self_rotate: bool) -> Logger:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level.value)

        if stream is True:
            self._add_stream_handler(logger, level)

        if file is True:
            logger_path = join(env_config.LOG_PATH, logger_name, f"{logger_name}.log")
            os.makedirs(os.path.dirname(logger_path), exist_ok=True)
            self._add_file_handler(logger, level, logger_path, self_rotate)

        return logger

    def _add_stream_handler(self, logger: Logger, level: LogLevel) -> None:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level.value)
        stream_handler.setFormatter(self.FORMATTER)
        logger.addHandler(stream_handler)

    def _add_file_handler(self, logger: Logger, level: LogLevel, logger_path: str, self_rotate: bool) -> None:
        if self_rotate:
            file_handler = logging.handlers.TimedRotatingFileHandler(
                filename=logger_path,
                when="midnight",
                interval=1,
                backupCount=7,
                encoding="utf-8",
            )
        else:
            file_handler = logging.handlers.WatchedFileHandler(
                filename=logger_path,
                mode="a",
                delay=False,
                encoding="utf-8",
            )

        file_handler.suffix = "%Y%m%d"
        file_handler.setLevel(level.value)
        file_handler.setFormatter(self.FORMATTER)
        logger.addHandler(file_handler)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def exception(self, message: str) -> None:
        formatted_traceback = textwrap.indent(traceback.format_exc(), "        ")
        self.logger.error(f"{message}\n{formatted_traceback}")
