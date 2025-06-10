from pydantic import Field
from pydantic_settings import BaseSettings

from image_test.logger.log_enum import LogLevel


class EnvSettings(BaseSettings):
    # ==========================================================
    # 1. Log Settings
    # ==========================================================

    LOG_LEVEL: LogLevel = Field(env="LOG_LEVEL", default=LogLevel.DEBUG)
    LOG_STREAM: bool = Field(env="LOG_STREAM", default=True)
    LOG_FILE: bool = Field(env="LOG_FILE", default=True)
    LOG_SELF_ROTATE: bool = Field(env="LOG_SELF_ROTATE", default=False)

    # Volume
    FILE_PATH: str = Field(env="FILE_PATH", default="/file")
    LOG_PATH: str = Field(env="LOG_PATH", default="/log")

    # ==========================================================
    # 2. Extracting Settings
    # ==========================================================

    SEMAPHORE_SIZE: int = Field(env="SEMAPHORE_SIZE", default=50)
    CHUNK_SIZE: int = Field(env="CHUNK_SIZE", default=10)

    PDF2IMAGE_MEMORY: bool = Field(env="PDF2IMAGE_MEMORY", default=True)
    PDF2IMAGE_DISK: bool = Field(env="PDF2IMAGE_DISK", default=True)
    PYMUPDF: bool = Field(env="PYMUPDF", default=True)
    PDFPLUMBER_MEMORY: bool = Field(env="PDFPLUMBER_MEMORY", default=True)
    PDFPLUMBER_MEMORY_CHUNK: bool = Field(env_config="PDFPLUMBER_MEMORY_CHUNK", default=True)
    PDFPLUMBER_DISK: bool = Field(env="PDFPLUMBER_DISK", default=True)


env_config = EnvSettings()
