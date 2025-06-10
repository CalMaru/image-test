import asyncio
import os
import re
from os.path import basename, join

from pdf2image import convert_from_path

from image_test.config import env_config
from image_test.image_parser.base import ImageParser
from image_test.logger.log_decorator import time_memory_logger


class Pdf2ImageDiskParser(ImageParser):
    _page_number_pattern = re.compile(r"-(\d+)\.png$")
    _semaphore = None

    def __init__(self):
        self._semaphore = asyncio.Semaphore(env_config.SEMAPHORE_SIZE)

    @time_memory_logger
    async def extract_images(self, pdf_file_path: str, image_dir_path: str) -> None:
        image_paths = await asyncio.to_thread(
            convert_from_path,
            pdf_path=pdf_file_path,
            output_folder=image_dir_path,
            fmt="png",
            paths_only=True,
        )

        await self.change_file_names(image_paths, image_dir_path)

    async def change_file_names(self, image_paths: list[str], image_dir_path: str) -> None:
        async def rename_with_semaphore(old_path: str):
            async with self._semaphore:
                if match := self._page_number_pattern.search(basename(old_path)):
                    new_path = join(image_dir_path, f"slide-{match.group(1)}.png")
                    await asyncio.to_thread(os.rename, old_path, new_path)

        tasks = [rename_with_semaphore(old_path) for old_path in image_paths]
        await asyncio.gather(*tasks)
