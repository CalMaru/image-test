from dependency_injector import containers, providers

from image_test.config import env_config
from image_test.logger.log_manager import LogManager


class LogContainer(containers.DeclarativeContainer):
    AccessLogger = providers.Singleton(
        LogManager,
        logger_name="ACCESS",
        level=env_config.LOG_LEVEL,
        stream=env_config.LOG_STREAM,
        file=env_config.LOG_FILE,
        self_rotate=env_config.LOG_SELF_ROTATE,
    )


log_container = LogContainer()
access_logger = log_container.AccessLogger()
