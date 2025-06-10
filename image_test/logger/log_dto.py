from time import time
from typing import Optional

from pydantic import BaseModel


class BaseLogFormat(BaseModel):
    class_name: str
    process_time: float
    peak_memory_usage: Optional[int]
    message: Optional[str]

    def __str__(self) -> str:
        log = f"{self.class_name:<15}|{self.process_time:>8.2f}sec|"

        if self.peak_memory_usage:
            peak_mb = self.peak_memory_usage / (1024 * 1024)
            log = f"{log}{peak_mb:<.4f} MB|"

        if self.message:
            log = f"{log}{self.message}"

        return log

    @classmethod
    def from_(
        cls,
        class_name: str,
        start_time: time,
        end_time: time,
        peak_memory_usage: Optional[int] = None,
        message: Optional[str] = None,
    ):
        return cls(
            class_name=class_name,
            process_time=end_time - start_time,
            peak_memory_usage=peak_memory_usage,
            message=message,
        )
