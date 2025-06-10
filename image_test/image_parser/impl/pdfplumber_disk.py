import asyncio
import os
import re
from os.path import join

import pdfplumber
from pdf2image import convert_from_path

from image_test.config import env_config
from image_test.image_parser.base import ImageParser
from image_test.logger.log_decorator import time_memory_logger


class PdfplumberDiskImageParser(ImageParser):
    _page_number_pattern = re.compile(r"-(\d+)\.png$")
    _semaphore = None

    def __init__(self):
        self._semaphore = asyncio.Semaphore(env_config.SEMAPHORE_SIZE)

    @time_memory_logger
    async def extract_images(self, pdf_file_path: str, image_dir_path: str) -> None:
        page_count = self._get_page_count(pdf_file_path)

        tasks = [self._save_images(pdf_file_path, image_dir_path, page + 1) for page in range(page_count)]
        await asyncio.gather(*tasks)

    async def _save_images(self, pdf_file_path: str, image_dir_path: str, page: int) -> None:
        async with self._semaphore:
            image_page_path = join(image_dir_path, str(page))
            os.makedirs(image_page_path, exist_ok=True)

            image_paths = await asyncio.to_thread(
                convert_from_path,
                pdf_path=pdf_file_path,
                output_folder=image_page_path,
                first_page=page,
                last_page=page,
                fmt="png",
                paths_only=True,
            )

            image_file_path = join(image_page_path, f"slide-{page}.png")
            os.rename(image_paths[0], image_file_path)

    @staticmethod
    def _get_page_count(pdf_file_path: str) -> int:
        with pdfplumber.open(pdf_file_path) as pdf:
            return len(pdf.pages)
